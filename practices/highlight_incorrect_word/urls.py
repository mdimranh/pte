from django.urls import path

from .views import *

urlpatterns = [
    path('highlight_incorrect_word', HighlightIncorrectWordCreateAPIView.as_view()),
    path('highlight_incorrect_word/<int:id>/update', HighlightIncorrectWordUpdateAPIView.as_view()),
    path('highlight_incorrect_words', HighlightIncorrectWordListAPIView.as_view()),
    path('highlight_incorrect_word/<int:pk>', HighlightIncorrectWordDetailsView.as_view())
]