from django.urls import path

from .views import *
from .answer import ReadAloudAnswerCreate

urlpatterns = [
    path('read_aloud/<pk>', ReadAloudView.as_view()),
    path('read_aloud', ReadAloudCreateView.as_view()),
    path('read_alouds', ReadAloudListView.as_view()),
    path('word_details', GetWordDetails.as_view()),
    path('read_alouds/create', ReadAloudAnswerCreate.as_view())
]