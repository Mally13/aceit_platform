from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.auth_views import *

urlpatterns = [
    path('account/password-reset/', include('django_rest_passwordreset.urls', namespace='user-password-reset')),
    path('account/register/', UserListCreate.as_view(), name='user-register'),
    path('account/login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='user-token-refresh'),
    path('account/change-password/', ChangePasswordView.as_view(), name="user-change-password"),
]
