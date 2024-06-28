from django.urls import path
from ..views.user_management_views import UserProfileView, UserRolesView

urlpatterns = [
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/roles/', UserRolesView.as_view(), name='user-roles'),
]
