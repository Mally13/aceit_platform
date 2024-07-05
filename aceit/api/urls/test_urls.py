from django.urls import path
from ..views import CategoryListView, TestListView, TestRetrieveView

urlpatterns = [
    path('tests/categories/', CategoryListView.as_view(), name='category-list'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestRetrieveView.as_view(), name='test-detail'),
    path('tests/category/tests/<int:category_id>/', TestListView.as_view(), name='categoty-test-list'),
]
