from django.urls import path

from .views import AnswerCreateView, AnswerListView

urlpatterns = [
    path("answers", AnswerListView.as_view()),
    path("answer", AnswerCreateView.as_view())
]