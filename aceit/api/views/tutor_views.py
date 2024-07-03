from rest_framework import generics, permissions
from ..models import Test
from ..serializers import TestSerializer
from ..permissions import IsTutor

class TutorTestCreateView(generics.CreateAPIView):
    """Handles GET and POST requests for Test model."""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def perform_create(self, serializer):
        """Sets the created_by field to the current user."""
        serializer.save(created_by=self.request.user)

class TutorDraftTestsView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def get_queryset(self):
        """
        Returns draft tests created by the authenticated user.
        """
        user = self.request.user
        return Test.objects.filter(created_by=user, status='draft')


class TutorCompletedTestsView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated,IsTutor]

    def get_queryset(self):
        """
        Returns completed tests created by the authenticated user.
        """
        user = self.request.user
        return Test.objects.filter(created_by=user, status='complete')
