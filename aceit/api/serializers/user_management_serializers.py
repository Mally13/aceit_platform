#!/usr/bin/env python3
"""
Module defines serializers for user data
"""
from rest_framework import serializers
from ..models import User

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes profile data"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture', 'phone_number', 'is_tutor', 'is_student')
        read_only_fields = ('email',)
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_picture': {'required': False},
            'phone_number': {'required': False},
            'is_tutor': {'required': False},
            'is_student': {'required': False},
        }

class UserRoleSerializer(serializers.ModelSerializer):
    """Serializes User roles data"""
    class Meta:
        model = User
        fields = ('is_tutor', 'is_student', 'is_staff')
