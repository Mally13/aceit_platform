from .auth_urls import urlpatterns as auth_urls
from .user_management_urls import urlpatterns as user_management_urls

urlpatterns = auth_urls + user_management_urls
