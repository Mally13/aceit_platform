#!/usr/bin/env python3
"""
Module for Test Views.
Includes:
    - test/tests retrieval
    - test response submission
    - test/tests results retrieval
"""
from decimal import Decimal
from django.db.models import Avg
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..models import (
    Test, Category, Question, StudentResponse, UserTestResult
)
from ..serializers import (
    TestSerializer, CategorySerializer,
    TestResponseSerializer, AttemptedTestsSerializer,
    AttemptedQuestionSerializer
)
from ..permissions import IsTutor
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
    """
    View handles submission of test responses by student.
    """
    serializer_class = TestResponseSerializer

    def create(self, request, *args, **kwargs):
        """
        Logic for handling test submission and marking.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        responses = serializer.validated_data['responses']
        test_id = kwargs['test_id']

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({'error': 'The test: test_id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        marks_attainable = 0
        student_marks = 0
        student = request.user
        questions = test.questions.all()
        for question in questions:
            marks_attainable += question.marks
            response_obj = None
            for response in responses:
                if response['question'] == question:
                    student_response = response['response']
                    try:
                        response_obj = StudentResponse.objects.get(
                            question=question,
                            student=student,
                        )
                        response_obj.response = student_response
                    except StudentResponse.DoesNotExist:
                        response_obj = StudentResponse.objects.create(
                            question=question,
                            student=student,
                            response=student_response
                        )
                    correct_answers = question.correct_answers
                    if set(student_response) == set(correct_answers):
                        response_obj.is_correct = True
                        student_marks += question.marks

            if response_obj is None:
                response_obj = StudentResponse.objects.create(
                    question=question,
                    student=student,
                    response=[],
                    is_correct=False
                )

            response_obj.save()

        percentage_score = (Decimal(student_marks) /
                            Decimal(marks_attainable)) * 100
        percentage_score = round(percentage_score, 2)
        try:
            user_test_result = UserTestResult.objects.get(
                test=test, student=student)
        except UserTestResult.DoesNotExist:
            user_test_result = UserTestResult.objects.create(
                test=test,
                student=student,
            )
        user_test_result.percentage_score = percentage_score
        user_test_result.save()

        return Response(
            {
                'test_id': test.id,
                'percentage_score': percentage_score
            },
            status=status.HTTP_201_CREATED)


class AttemptedTestsView(generics.ListAPIView):
    """
    View handles GET request for all tests that a student has completed.
    """
    serializer_class = AttemptedTestsSerializer

    def get_queryset(self):
        """
        Filters out only stored results of authenticated user
        """
        user = self.request.user
        return UserTestResult.objects.filter(student=user)

    def list(self, request, *args, **kwargs):
        """
        Logic for listing all tests completed by a user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tests_average = queryset.aggregate(
            average_score=Avg('percentage_score', default=0))
        tests_average = round(tests_average['average_score'], 2)

        return Response(
            {
                'tests': serializer.data,
                'tests_average': tests_average
            },
            status=status.HTTP_200_OK
        )


class AttemptedTestView(generics.RetrieveAPIView):
    """
    View handles GET request for a single test that a student has completed.

    The test is returned together with the responses of the student.
    """
    serializer_class = AttemptedQuestionSerializer

    def get_queryset(self):
        """
        """
        test_id = self.kwargs['test_id']
        return Question.objects.filter(test__id=test_id)

    def retrieve(self, request, *args, **kwargs):
        """
        Logic for retrieving test and responses.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={
                                         'student': request.user})
        test_id = kwargs['test_id']
        try:
            test_result = UserTestResult.objects.get(
                test__id=test_id, student=request.user)
        except UserTestResult.DoesNotExist:
            return Response(
                {'error': f'There is no record of atttempted test_id: {test_id} by user.'}, status=status.HTTP_404_NOT_FOUND
            )

        test_result_serializer = AttemptedTestsSerializer(test_result)
        return Response(
            {
                'questions_responses': serializer.data, 'test_result': test_result_serializer.data
            },
            status=status.HTTP_200_OK
        )
