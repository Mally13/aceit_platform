from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.auth_views import *

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name="change_password"),
]
