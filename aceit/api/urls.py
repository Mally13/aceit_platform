from django.urls import path
from .views.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register')
]
