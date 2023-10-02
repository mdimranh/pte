from django.urls import path

# from .summarize import SummarizeAnswerCreateView
from .views import SummarizeAnswerListView

urlpatterns = [
    # path("summarize/answer", SummarizeAnswerCreateView.as_view()),
    path("summarize/<int:pk>/answers", SummarizeAnswerListView.as_view())
]