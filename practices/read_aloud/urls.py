from django.urls import path

from .views import *
from .answer import ReadAloudAnswerCreate

urlpatterns = [
    path('read_aloud/<int:pk>', ReadAloudView.as_view()),
    path('read_aloud', ReadAloudCreateView.as_view()),
    path('read_alouds', ReadAloudListView.as_view()),
    path('word_details', GetWordDetails.as_view()),
    path('read_aloud/<int:pk>/answer', SummarizeAnswerListView.as_view()),
    path('read_alouds/answer', ReadAloudAnswerCreate.as_view()),
    path('read_aloud/<int:pk>/my_answer', MyAnswerListView.as_view())
]