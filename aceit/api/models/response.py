#!/usr/bin/env python3
"""
Module for model for test responses.
"""
from django.db import models

from .question import Question
from .user import User


class Response(models.Model):
    """
    Model for test responses.
    """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='student_response'
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responses'
    )
    is_correct = models.BooleanField()
    response = models.JSONField()

    def __str__(self):
        """
        Returns a string representation of the response.

        In this case informs about the question to which the response
        belongs and the student who made the response.
        """
        return 'Response by student: {self.student.id} to question {self.question.id}'
