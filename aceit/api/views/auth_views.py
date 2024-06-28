#!/usr/bin/env python3
"""
Module for views
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from ..serializers.auth_serializers import (
    UserRegistrationSerializer, CustomTokenObtainPairSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Create API view for user registration.
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Obtain both an access token and a refresh token for a user.

    This view also includes the user data in the response on login.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
