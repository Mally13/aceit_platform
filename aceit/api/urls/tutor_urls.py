from django.urls import path
from ..views import TutorCompletedTestsView, TutorDraftTestsView, TutorTestCreateView, TutorTestRetrieveUpdateDestroyView, QuestionTutorCreateAPIView, QuestionTutorAPIView

urlpatterns = [
    path('tutor/completed-tests/', TutorCompletedTestsView.as_view(), name='tutor-completed-tests'),
    path('tutor/draft-tests/', TutorDraftTestsView.as_view(), name='tutor-draft-tests'),
    path('tutor/test/', TutorTestCreateView.as_view(), name='tutor-test-create'),
    path('tutor/tests/<int:test_id>/', TutorTestRetrieveUpdateDestroyView.as_view(), name='test-retrieve-update-destroy'),
    path('tutor/tests/<int:test_id>/questions/<int:question_id>/', QuestionTutorAPIView.as_view(), name='question-detail'),
    path('tutor/tests/question/<int:test_id>/', QuestionTutorCreateAPIView.as_view(), name='add-question'),
]
