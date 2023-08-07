from django.urls import path

from .views import SummarizeAnswerListView
from .summarize import SummarizeAnswerCreateView

urlpatterns = [
    path("summarize/answer", SummarizeAnswerCreateView.as_view()),
    path("summarize/<int:pk>/answers", SummarizeAnswerListView.as_view())
]