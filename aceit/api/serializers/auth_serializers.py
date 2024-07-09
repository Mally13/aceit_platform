#!/usr/bin/env python3
"""
Module for Auth Serializers
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .user_management_serializers import UserProfileSerializer

from ..models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes user registration data.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'profile_picture', 'is_tutor', 'is_student')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate(self, attrs):
        """Validates password and password2 match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        """Creates a new user."""
        validated_data.pop('password2')
        validated_data['is_student'] = True
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the TokenObtainPairSerializer to include user data in the response.
    """
    def validate(self, attrs):
        """
        Validates user credentials and returns token pair plus
        user data in the response.
        """
        data = super().validate(attrs)
        user = self.user
        profile_data = UserProfileSerializer(user).data
        data.update({
            'user_data': {
                'profile_data': profile_data
            }
        })

        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializes old_password and new_password for changing user password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

