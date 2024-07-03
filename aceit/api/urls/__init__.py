from .auth_urls import urlpatterns as auth_urls
from .test_urls import urlpatterns as test_urls
from .tutor_urls import urlpatterns as tutor_urls
from .user_management_urls import urlpatterns as user_management_urls
from django.urls import path
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


doc_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = doc_urls + auth_urls + user_management_urls + test_urls + tutor_urls
