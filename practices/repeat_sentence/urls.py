from django.urls import path

from .views import *

urlpatterns = [
    path('repeat_sentence', RepeatSentenceCreateAPIView.as_view()),
    path('repeat_sentences', RepeatSentenceListAPIView.as_view()),
    path('repeat_sentence/<int:pk>', RepeatSentenceDetailsView.as_view()),
    path('repeat_sentence/<int:pk>/answer', RepeatSentenceAnswerListView.as_view()),
    # path('repeat_sentence/answer', RepeatSentenceAnswerCreateView.as_view()),
    path('repeat_sentence/<int:pk>/my_answer', MyAnswerListView.as_view())
]