#!/usr/bin/env python3
from rest_framework import serializers
from ..models import Test, Question, Subject


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_type', 'image', 'answers')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class SubjectSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    education_level = serializers.CharField()
    pathway = serializers.CharField()
    track = serializers.CharField()
    grade = serializers.CharField()   


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    subject_fields = SubjectSerializer(write_only=True)

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'created_by', 'subject', 'term', 'duration', 'questions', 'is_ready',
                  'subject_fields')
        read_only_fields = ('created_by', 'id', 'subject',)

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        subject_fields = validated_data.pop('subject_fields')
        subject = Subject.objects.get(**subject_fields)
        created_by = self.context['request'].user
        test = Test.objects.create(created_by=created_by, subject=subject, **validated_data)
        for question_data in questions_data:
            Question.objects.create(test=test, **question_data)
        return test
