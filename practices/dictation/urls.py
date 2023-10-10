from django.urls import path

from .views import *

urlpatterns = [
    path('dictation', DictationCreateAPIView.as_view()),
    path('dictations', DictationListAPIView.as_view()),
    path('dictation/<int:pk>', DictationDetailsView.as_view()),
    path('dictation/<int:pk>/answer', DictationAnswerListView.as_view()),
    path('dictation/answer', DictationAnswerCreateView.as_view()),
    path('dictation/<int:pk>/my_answer', MyAnswerListView.as_view())
]