from django.urls import path
from ..views import CategoryListView, TestCreateView, TestListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/create/', TestCreateView.as_view(), name='test-create'),
]