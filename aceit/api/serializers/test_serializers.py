from rest_framework import serializers
from ..models import Test

class TestSerializer(serializers.ModelSerializer):
    """Defines Test Serializer"""
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'category', 'created_by']