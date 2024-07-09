#!/usr/bin/env python3
"""
Module defines test serializers
"""
from rest_framework import serializers
from ..models import Test, Question
from .question_serializers import QuestionSerializer


class TestSerializer(serializers.ModelSerializer):
    """Defines Test Serializer"""
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'created_by', 'questions']

    def get_created_by(self, obj):
        """Get the first and last name of the tutor"""
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

class TestListSerializer(serializers.ModelSerializer):
    """Defines Test List Serializer"""
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'created_by']

    def get_created_by(self, obj):
        """Get the first and last name of the tutor"""
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        


class TestTutorSerializer(serializers.ModelSerializer):
    """Serializes test data of the tutor"""
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'status', 'questions']

    def create(self, validated_data):
        """Remove questions from the validated data"""
        validated_data.pop('questions', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        instance = super().update(instance, validated_data)
        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id:
                question = Question.objects.get(id=question_id, test=instance)
                for attr, value in question_data.items():
                    setattr(question, attr, value)
                question.save()
            else:
                Question.objects.create(test=instance, **question_data)
        return instance
