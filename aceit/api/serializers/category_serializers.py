#!/usr/bin/env python3
"""
Module for Category Serializers
"""
from rest_framework import serializers
from ..models import Category
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    """Serializes test categories"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    @extend_schema_field(str)
    def get_children(self, obj):
        """Gets the children of a category"""
        return CategorySerializer(obj.get_children(), many=True).data
