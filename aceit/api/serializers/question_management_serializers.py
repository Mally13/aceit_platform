#!/usr/bin/env python3
from rest_framework import serializers
from ..models import Question, Test


class QuestionManagementSerializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_type', 'image', 'answers', 'test_id')
        extra_kwargs = {
            'id': {'read_only': True},
            'test_id': {'write_only': True},
        }

    def create(self, validated_data):
        test_id = validated_data.pop('test_id')
        test = Test.objects.get(id=test_id)
        return Question.objects.create(test=test, **validated_data)
