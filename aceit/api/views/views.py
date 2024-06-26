#!/usr/bin/env python3
"""
Module for views
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import User
from ..serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    Create API view for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
