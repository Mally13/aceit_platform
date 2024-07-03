from rest_framework import generics, permissions, status
from ..models import Test, Category
from ..serializers import TestSerializer, CategorySerializer
from ..permissions import IsTutor
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TestRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Handles GET and PUT requests for a single Test instance."""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensures only the owner can update their test."""
        user = self.request.user
        if self.request.method == 'PUT':
            return Test.objects.filter(created_by=user)
        return super().get_queryset()

class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally restricts the returned tests to a given category,
        by filtering against a `category_id` query parameter in the URL.
        Also restricts the returned tests based on the user's role and test status.
        """
        category_id = self.request.query_params.get('category_id')
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                tests = Test.objects.filter(category__in=category.get_descendants(include_self=True))
            except Category.DoesNotExist:
                raise NotFound(detail="Category not found.")
        else:
            tests = Test.objects.all()
            return tests.filter(status='complete')

    def list(self, request, *args, **kwargs):
        """
        Override the list method to handle custom error response.
        """
        try:
            queryset = self.get_queryset()
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

