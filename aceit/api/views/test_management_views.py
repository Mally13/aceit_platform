from rest_framework import viewsets
from django_filters import rest_framework as filters

from ..models import Test, Question
from ..serializers import TestSerializer, QuestionManagementSerializer
from ..filters import TestFilter


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TestFilter


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionManagementSerializer
