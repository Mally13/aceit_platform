#!/usr/bin/env python3
"""
Module defines serializers for questions
"""
from rest_framework import serializers
from ..models import Question


class QuestionTutorSerializer(serializers.ModelSerializer):
    """Serializes the question data for the tutor"""
    class Meta:
        model = Question
        fields = ['id', 'test', 'images', 'question_text',
                  'options', 'correct_answers', 'explanation']

    def __init__(self, *args, **kwargs):
        super(QuestionTutorSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields.pop('test')


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes question data for the student who is yet to do a test
    """
    reveal_answer_after_completion = serializers.BooleanField(read_only=True)
    reveal_explanation_after_completion = serializers.BooleanField(
        read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'images', 'question_text', 'options',
                  'reveal_answer_after_completion', 'reveal_explanation_after_completion']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     user = self.context['request'].user
    #     if user.has_completed_test(instance.test):
    #         data['correct_answer'] = instance.correct_answer
    #         data['explanation'] = instance.explanation
    #     return data
