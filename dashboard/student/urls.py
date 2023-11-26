from django.urls import path

from .views import ExamCountdownView, TargetScoreView

urlpatterns = [
    path("exam_countdown", ExamCountdownView.as_view()),
    path("target_score", TargetScoreView.as_view()),
]
