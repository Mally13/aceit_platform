from rest_framework import serializers
from ..models import Test, Question
from .question_serializers import QuestionSerializer

class TestSerializer(serializers.ModelSerializer):
    """Defines Test Serializer"""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'status', 'created_by', 'questions']

    def __init__(self, *args, **kwargs):
        super(TestSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields.pop('questions')
            self.fields.pop('created_by')

class TestTutorSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'display_picture', 'category', 'status', 'created_by', 'questions']

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


