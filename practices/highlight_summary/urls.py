from django.urls import path

from .views import *

urlpatterns = [
    path('highlight_summary', HighlightSummaryCreateAPIView.as_view()),
    path('highlight_summary/<int:id>/update', HighlightSummaryUpdateAPIView.as_view()),
    path('highlight_summarys', HighlightSummaryListAPIView.as_view()),
    path('highlight_summary/<int:pk>', HighlightSummaryDetailsView.as_view()),
    path('highlight_summary/<int:pk>/answer', HighlightSummaryAnswerListView.as_view()),
    path('highlight_summary/answer', HighlightSummaryAnswerCreateView.as_view()),
    path('highlight_summary/<int:pk>/my_answer', MyAnswerListView.as_view())
]