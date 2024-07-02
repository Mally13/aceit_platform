from django.urls import path
from ..views.user_management_views import *
"""Contains all the user management urls"""


urlpatterns = [
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/roles/', UserRolesView.as_view(), name='user-roles'),
]
