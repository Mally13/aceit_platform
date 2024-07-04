from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.test_management_views import TestViewSet

router = DefaultRouter()
router.register(r'tests', TestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
