from rest_framework import serializers

from ..models import (
    UserTestResult, Test, Question, StudentResponse
)


class AttemptedTestsSerializer(serializers.ModelSerializer):
    """
    Serializes tests that a user has already completed.
    """
    class Meta:
        model = UserTestResult
        fields = ['test', 'percentage_score']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'options', 'correct_answers',
            'explanation', 'marks', 'images', 'has_multiple_correct_answers'
        ]


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse
        fields = ['question', 'response', 'is_correct']


class AttemptedQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    student_response = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['question', 'student_response']

    def get_student_response(self, obj):
        student = self.context['student']
        response = StudentResponse.objects.get(student=student, question=obj)
        return StudentResponseSerializer(response).data
