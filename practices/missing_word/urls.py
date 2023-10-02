from django.urls import path

from .views import *

urlpatterns = [
    path('missing_word', MissingWordCreateAPIView.as_view()),
    path('missing_words', MissingWordListAPIView.as_view()),
    path('missing_word/<int:pk>', MissingWordDetailsView.as_view()),
    path('missing_word/<int:pk>/answer', MissingWordAnswerListView.as_view()),
    path('missing_word/answer', MissingWordAnswerCreateView.as_view()),
    path('missing_word/<int:pk>/my_answer', MyAnswerListView.as_view())
]