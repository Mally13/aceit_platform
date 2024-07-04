#!/usr/bin/env python3
"""
Module defines app Test model
"""
from django.db import models

from .user import User
from .subject import Subject


class Test(models.Model):
    """
    Defines a Test model.
    """
    TERM_CHOICES = (
        ('1', 'Term1'),
        ('2', 'Term 2'),
        ('3', 'Term 3'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    term = models.CharField(max_length=1, choices=TERM_CHOICES)
    duration = models.DurationField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the object.

        In this case, it returns the title of the Test object.
        """
        return self.title
