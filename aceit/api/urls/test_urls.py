from django.urls import path
from ..views import CategoryListView, TestListView

urlpatterns = [
    path('tests/categories/', CategoryListView.as_view(), name='category-list'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/category/tests/', TestListView.as_view(), name='categoty-test-list'),
]
