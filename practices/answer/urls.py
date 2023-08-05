from django.urls import path

from .views import AnswerCreateView, AnswerListView, SummarizeAnswerListView
from .summarize import SummarizeAnswerCreateView

urlpatterns = [
    path("answers", AnswerListView.as_view()),
    path("answer", AnswerCreateView.as_view()),
    path("summarize/answer", SummarizeAnswerCreateView.as_view()),
    path("summarize/<int:pk>/answers", SummarizeAnswerListView.as_view())
]