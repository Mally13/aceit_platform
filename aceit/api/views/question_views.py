# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Test, Question
from ..serializers import QuestionSerializer
from ..permissions import IsTutor

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Question.objects.filter(test_id=test_id)