#!/usr/bin/env python3
"""Contains Question Views"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models import Test, Question
from ..serializers import QuestionSerializer
from ..permissions import IsTutor


class QuestionListView(generics.ListAPIView):
    """Lists all questions in a test"""
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the questions based on the test id
        """
        test_id = self.kwargs['test_id']
        return Question.objects.filter(test_id=test_id)
