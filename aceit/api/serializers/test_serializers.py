from rest_framework import serializers
from ..models import Test

class TestSerializer(serializers.ModelSerializer):
    """Defines Test Serializer"""
    class Meta:
        model = Test
        fields = ['id', 'title', 'description','display_picture', 'category', 'status', 'created_by']
        read_only_fields = ['created_by']
    
    def to_representation(self, instance):
        """Customize the representation of the data for GET requests."""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            return representation
        representation.pop('created_by')
        return representation

    def create(self, validated_data):
        """Sets created_by field to the current user."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Ensures only the owner can update the test."""
        request = self.context['request']
        if request.user != instance.created_by:
            raise serializers.ValidationError("You do not have permission to edit this test.")
        return super().update(instance, validated_data)
