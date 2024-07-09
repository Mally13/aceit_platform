#!/usr/bin/env python3
"""
Module for Test responses Serializers
"""
from rest_framework import serializers

from ..models import StudentResponse


class ResponseSerializer(serializers.ModelSerializer):
    """
    Serializes test responses.

    Ensures question id and response are included in request body.
    """
    class Meta:
        model = StudentResponse
        fields = ['question', 'response']


class TestResponseSerializer(serializers.Serializer):
    """
    Serializes incoming responses for a test.
    """
    test_id = serializers.IntegerField()
    responses = ResponseSerializer(many=True)
