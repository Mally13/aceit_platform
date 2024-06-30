#!/usr/bin/env python3
"""
Module for views
"""
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from ..models import User
from ..serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)


class UserListCreate(generics.ListCreateAPIView):
    """
    Create API view for user registration.

    GET method returns a list of all users.
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


class ChangePasswordView(APIView):
    """
    API view for changing the user's password.

    POST method allows the logged in user to change their password.
    """
    @extend_schema(responses=ChangePasswordSerializer)
    def post(self, request, *args, **kwargs):
        """
        Handles POST request to change the user's password.
        """
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not user.check_password(old_password):
                return Response(
                    {'error': 'Incorrect old password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': 'Password changed successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
