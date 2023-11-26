from django.urls import path
from .views import *

urlpatterns = [
    path('summarize', SummarizeCreateView.as_view()),
    path('summarize/<int:id>/update', SummarizeUpdateView.as_view()),
    path('summarize/<int:pk>', SummarizeDetailView.as_view()),
    path('summarizes', SummarizeListView.as_view()),
    path('spoken/summarize', SummarizeSpokenCreateView.as_view()),
    path('spoken/summarize/<int:id>/update', SummarizeSpokenUpdateView.as_view()),
    path('spoken/summarize/<int:pk>', SummarizeSpokenDetailView.as_view()),
    path('spoken/summarizes', SummarizeSpokenListView.as_view())
]