from django.urls import path
from ..views import SubmitTestView, AttemptedTestsView, AttemptedTestView


urlpatterns = [
    path('student/tests/attempted', AttemptedTestsView.as_view(),
         name='student-attempted-tests'),
    path('student/tests/attempted/<int:test_id>', AttemptedTestView.as_view(),
         name='student-attempted-test'),
    path(
        'student/tests/<int:test_id>/responses/', SubmitTestView.as_view(), name='student-submit-test'
    ),
]
