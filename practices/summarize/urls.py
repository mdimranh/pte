from django.urls import path
from .views import *

urlpatterns = [
    path('summarize', SummarizeCreateView.as_view()),
    path('summarize/<int:pk>', SummarizeDetailView.as_view()),
    path('summarizes', SummarizeListView.as_view())
]