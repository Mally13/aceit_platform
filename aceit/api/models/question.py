#!/usr/bin/env python3
"""
Module defines app Question model
"""
from django.db import models

from .test import Test


class Question(models.Model):
    """
    This class defines the model for a question. 

    Attribute test is a foreign key to the Test model to associate
    the question with a test.
    """
    QUESTION_TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice Question'),
        ('TEXT', 'Text Question'),
    )

    question_text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPE_CHOICES)
    answers = models.JSONField()
    # explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the question.

        In this case returns the question text.
        """
        return self.question_text
