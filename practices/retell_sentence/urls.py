from django.urls import path

from .views import *

urlpatterns = [
    path('retell_sentence', RetellSentenceCreateAPIView.as_view()),
    path('retell_sentences', RetellSentenceListAPIView.as_view()),
    path('retell_sentence/<int:pk>', RetellSentenceDetailsView.as_view()),
    path('retell_sentence/<int:pk>/answer', RetellSentenceAnswerListView.as_view()),
    # path('retell_sentence/answer', RetellSentenceAnswerCreateView.as_view()),
    path('retell_sentence/<int:pk>/my_answer', MyAnswerListView.as_view())
]