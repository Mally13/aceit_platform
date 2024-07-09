#!/usr/bin/env python3
"""
Module for model for user test results.
"""
from django.db import models
from decimal import Decimal

from .test import Test
from .user import User


class UserTestResult(models.Model):
    """
    Model for user test results.
    """
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='user_test_results'
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_test_results'
    )
    percentage_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00')
    )

    def __str__(self):
        """
        Returns a string representation of the user test result.

        In this case informs about the test to which the user test
        result belongs and the student who made the test.
        """
        return 'User test result by student: {self.student.id} to test {self.test.id}: {self.percentage_score}'
