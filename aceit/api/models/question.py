#!/usr/bin/env python3
"""
Module defines app's question model
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField

from .test import Test

class Question(models.Model):
    question_text = models.TextField()
    options = ArrayField(models.TextField())
    correct_answers = ArrayField(models.TextField())
    explanation = models.TextField()
    has_multiple_correct_answers = models.BooleanField()
    marks = models.IntegerField()
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='questions')
    images = models.ImageField(
        upload_to='question_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.id} for {self.test.title}"
