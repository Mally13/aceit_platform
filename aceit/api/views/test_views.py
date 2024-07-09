#!/usr/bin/env python3
"""
Module for test views
"""

from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from decimal import Decimal

from ..models import Test, Category, Question, StudentResponse, UserTestResult
from ..serializers import TestSerializer, CategorySerializer, TestListSerializer, TestResponseSerializer
from ..permissions import IsTutor


class CategoryListView(generics.ListAPIView):
    """Lists all Categories and their child categories"""
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TestRetrieveView(generics.RetrieveAPIView):
    """Handles GET requests a single Test instance."""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TestListView(generics.ListAPIView):
    """Handles GET request for all tests"""
    serializer_class = TestListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally restricts the returned tests to a given category,
        by filtering against a `category_id` query parameter in the URL.
        Also restricts the returned tests based on the test status.
        """
        category_id = self.kwargs.get('category_id')
        tests = Test.objects.filter(status='complete')

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                descendant_categories = category.get_descendants(
                    include_self=True)
                tests = tests.filter(category__in=descendant_categories)
            except Category.DoesNotExist:
                raise NotFound(detail="Category not found.")

        return tests

    def list(self, request, *args, **kwargs):
        """
        Override the list method to handle custom error response.
        """
        try:
            queryset = self.get_queryset()
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubmitTestView(generics.CreateAPIView):
    serializer_class = TestResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data['test_id']
        responses = serializer.validated_data['responses']

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({'error': 'The test: test_id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        marks_attainable = 0
        student_marks = 0
        student = request.user

        for response_data in responses:
            question_id = response_data['question']
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return (Response({'error': 'The question: question_id does not exist'}, status=status.HTTP_404_NOT_FOUND))

            response = response_data['response']
            response_obj = StudentResponse.objects.create(
                question=question,
                student=student,
                is_correct=False,
                response=response
            )

            correct_answers = question.correct_answers
            marks_attainable += question.marks
            if response.sort() == correct_answers.sort():
                response_obj.is_correct = True
                student_marks += question.marks
            response_obj.save()

        percentage_score = (Decimal(student_marks) /
                            Decimal(marks_attainable)) * 100
        percentage_score = round(percentage_score, 2)

        UserTestResult.objects.create(
            test=test,
            student=student,
            percentage_score=percentage_score
        )

        return Response({'percentage_score': percentage_score}, status=status.HTTP_201_CREATED)
