#!/usr/bin/env python3
"""
Module for Serializers
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes user registration data.

    Fields:
        email (str): User's email.
        first_name (str): User's first name.
        last_name (str): User's last name.
        password (str): User's password.
        password2 (str): Confirmation of user's password.
        profile_picture (str): User's profile picture URL.
        is_tutor (bool): Specifies if user is a tutor.

    Methods:
        validate(self, attrs): Validates if password and password2 match.
        create(self, validated_data): Creates a new user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'profile_picture', 'is_tutor')
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
        data.update({
            'user_data': {
                # will return the required user data
            }
        })

        return data
