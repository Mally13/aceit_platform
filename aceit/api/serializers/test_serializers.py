#!/usr/bin/env python3
"""
Module defines test serializers
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ..models import Test, Question
from .question_serializers import QuestionSerializer, QuestionTutorSerializer


class TestSerializer(serializers.ModelSerializer):
    """Defines Test Serializer"""
    questions = QuestionSerializer(many=True, read_only=True)
    num_questions = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'duration', 'term', 'num_questions', 'created_by', 'questions']

    @extend_schema_field(serializers.StringRelatedField)
    def get_category(self, obj):
        """Get the category of the test"""
        return f"{obj.category.parent.name} {obj.category.name}"

    @extend_schema_field(serializers.StringRelatedField)
    def get_created_by(self, obj):
        """Get the first and last name of the tutor"""
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    @extend_schema_field(serializers.StringRelatedField)
    def get_num_questions(self, obj):
        """Get the number of questions associated with this test"""
        return obj.questions.count()

class TestListSerializer(serializers.ModelSerializer):
    """Defines Test List Serializer"""
    created_by = serializers.SerializerMethodField()
    num_questions = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'duration', 'term', 'num_questions', 'created_by']

    @extend_schema_field(serializers.StringRelatedField)
    def get_created_by(self, obj):
        """Get the first and last name of the tutor"""
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    @extend_schema_field(serializers.StringRelatedField)
    def get_category(self, obj):
        """Get the category of the test"""
        return f"{obj.category.parent.name} {obj.category.name}"
        
    @extend_schema_field(serializers.StringRelatedField)
    def get_num_questions(self, obj):
        """Get the number of questions associated with this test"""
        return obj.questions.count()
class TestTutorSerializer(serializers.ModelSerializer):
    """Serializes test data of the tutor"""
    questions = QuestionTutorSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description',  'display_picture', 'category', 'duration', 'term', 'status', 'questions']

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

class NewTestTutorSerializer(serializers.ModelSerializer):
    """Serializes test data of the tutor"""

    class Meta:
        model = Test
        fields = ['title', 'description',  'display_picture', 'category', 'duration', 'term', 'status']

class TestListTutorSerializer(serializers.ModelSerializer):
    """Serializes test data of the tutor"""
    num_questions = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'duration', 'term', 'num_questions']
    
    @extend_schema_field(serializers.StringRelatedField)
    def get_num_questions(self, obj):
        """Get the number of questions associated with this test"""
        return obj.questions.count()
