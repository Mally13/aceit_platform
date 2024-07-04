from .auth_urls import urlpatterns as auth_urls
from .user_management_urls import urlpatterns as user_management_urls
from .test_management_urls import urlpatterns as test_management_urls
from .question_management_urls import urlpatterns as question_management_urls

urlpatterns = auth_urls + user_management_urls + test_management_urls + question_management_urls
