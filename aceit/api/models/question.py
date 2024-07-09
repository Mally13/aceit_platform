#!/usr/bin/env python3
"""
Module defines app's question model
"""
from django.db import models

from .test import Test

class Question(models.Model):
    question_text = models.TextField()
    options = models.JSONField()
    correct_answers = models.JSONField()
    explanation = models.TextField()
    has_multiple_correct_answers = models.BooleanField()
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='questions')
    images = models.ImageField(
        upload_to='question_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.id} for {self.test.title}"
