from rest_framework import generics, permissions
from ..models import Test, Category
from ..serializers import TestSerializer, CategorySerializer
from ..permissions import IsTutor

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            return Test.objects.filter(category__in=category.get_descendants(include_self=True))
        return Test.objects.none()
