#!/usr/bin/env python3
"""
Module for Test responses Serializers
"""
from rest_framework import serializers

from ..models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """
    Serializes test responses.
    """
    class Meta:
        model = Response
        fields = ['question', 'response']


class TestResponseSerializer(serializers.Serializer):
    """
    Serializes incoming responses for a test.
    """
    test_id = serializers.IntegerField()
    responses = ResponseSerializer(many=True)
