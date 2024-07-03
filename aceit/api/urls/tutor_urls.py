from django.urls import path
from ..views import TutorCompletedTestsView, TutorDraftTestsView, TutorTestCreateView

urlpatterns = [
    path('tutor/completed-tests/', TutorCompletedTestsView.as_view(), name='tutor-completed-tests'),
    path('tutor/draft-tests/', TutorDraftTestsView.as_view(), name='tutor-draft-tests'),
    path('tutor/test/create/', TutorTestCreateView.as_view(), name='tutor-test-create'),
]
