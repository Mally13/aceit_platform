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


class TestRetrieveView(generics.RetrieveAPIView):
    """Handles GET requests for all or a single Test instance."""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally restricts the returned tests to a given category,
        by filtering against a `category_id` query parameter in the URL.
        Also restricts the returned tests based on the test status.
        """
        category_id = self.kwargs.get('category_id')
        tests = Test.objects.filter(status='complete')

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                descendant_categories = category.get_descendants(
                    include_self=True)
                tests = tests.filter(category__in=descendant_categories)
            except Category.DoesNotExist:
                raise NotFound(detail="Category not found.")

        return tests

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