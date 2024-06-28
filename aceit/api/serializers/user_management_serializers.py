from rest_framework import serializers
from ..models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture', 'phone_number', 'is_tutor')
        read_only_fields = ('email',)  # Ensure email is read-only


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_tutor',)
