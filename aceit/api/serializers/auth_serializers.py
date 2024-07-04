#!/usr/bin/env python3
"""
Module for Serializers
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
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'profile_picture', 'phone_number','is_tutor')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate(self, attrs):
        """Validates password and password2 match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        """Creates a new user."""
        validated_data.pop('password2')
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
        user_profile = UserProfileSerializer(user).data
        data.update({
            'user_data': {
                'user_profile': user_profile
                # more data to be returned
            }
        })

        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializes old_password and new_password for changing user password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

