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
        fields = ['id', 'question_text', 'images', 'has_multiple_correct_answers', 'marks',
                  'options', 'correct_answers', 'explanation']

class NewQuestionTutorSerializer(serializers.ModelSerializer):
    """Serializes the question data for the tutor"""
    class Meta:
        model = Question
        fields = ['question_text', 'images', 'has_multiple_correct_answers', 'marks',
                  'options', 'correct_answers', 'explanation']



class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes question data for the student who is yet to do a test
    """
    class Meta:
        model = Question
        fields = ['id', 'test', 'images', 'question_text', 'options', 'has_multiple_correct_answers']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     user = self.context['request'].user
    #     if user.has_completed_test(instance.test):
    #         data['correct_answer'] = instance.correct_answer
    #         data['explanation'] = instance.explanation
    #     return data
