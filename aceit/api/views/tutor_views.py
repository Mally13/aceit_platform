#!/usr/bin/env python3
"""
Module for Tutorviews
"""
from rest_framework import generics, permissions, exceptions, status
from rest_framework.response import Response

from ..models import Test, Question
from ..serializers import TestTutorSerializer, QuestionTutorSerializer
from ..permissions import IsTutor


class TutorTestCreateView(generics.CreateAPIView):
    """Handles POST requests for Test model."""
    queryset = Test.objects.all()
    serializer_class = TestTutorSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def perform_create(self, serializer):
        """Sets the created_by field to the current user."""
        serializer.save(created_by=self.request.user)

class TutorDraftTestsView(generics.ListAPIView):
    """A view to handle tutors drafts"""
    serializer_class = TestTutorSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def get_queryset(self):
        """
        Returns draft tests created by the authenticated user.
        """
        user = self.request.user
        return Test.objects.filter(created_by=user, status='draft')


class TutorCompletedTestsView(generics.ListAPIView):
    """A view to handle tutors completed views"""
    serializer_class = TestTutorSerializer
    permission_classes = [permissions.IsAuthenticated,IsTutor]

    def get_queryset(self):
        """
        Returns completed tests created by the authenticated user.
        """
        user = self.request.user
        return Test.objects.filter(created_by=user, status='complete')

class TutorTestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET, PUT, PATCH, and DELETE requests for a single Test instance."""
    queryset = Test.objects.all()
    serializer_class = TestTutorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensures only the owner can update or delete their test."""
        user = self.request.user
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Test.objects.filter(created_by=user)
        return super().get_queryset()

    def get_object(self):
        """Ensures that the user can only retrieve, update, or delete their own test."""
        test_id = self.kwargs['test_id']
        obj = generics.get_object_or_404(self.get_queryset(), id=test_id)
        if obj.created_by != self.request.user:
            raise exceptions.PermissionDenied("You do not have permission to access this test.")
        return obj

    def retrieve(self, request, *args, **kwargs):
        """Handles GET request for a single Test instance."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Handles PUT and PATCH requests for a single Test instance."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """Saves the updated instance."""
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Handles DELETE request for a single Test instance."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """Deletes the instance."""
        instance.delete()
# class TutorQuetionCreateView(generics.CreateAPIView):
#     """Handles POST requests for Question model."""
#     queryset = Test.objects.all()
#     serializer_class = TestTutorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsTutor]

class QuestionTutorAPIView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    """Handles question views for the tutor"""
    queryset = Question.objects.all()
    serializer_class = QuestionTutorSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(test__created_by=user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('question_id'))
        return obj

    def perform_create(self, serializer):
        test_id = self.kwargs.get('test_id')
        test = generics.get_object_or_404(Test, pk=test_id)
        serializer.save(test=test)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class QuestionTutorCreateAPIView(generics.CreateAPIView):
    """Enables a user to POST a question"""
    queryset = Question.objects.all()
    serializer_class = QuestionTutorSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def perform_create(self, serializer):
        test_id = self.kwargs.get('test_id')
        test = generics.get_object_or_404(Test, pk=test_id)
        serializer.save(test=test)
