from django.urls import path
from .views import *

urlpatterns = [
    path("witting_mocktest", WrittingMocktestView.as_view()),
    path("witting_mocktests", WrittingMocktestListView.as_view()),
    path("witting_mocktest/<int:id>", WrittingMocktestUpdateDeleteView.as_view()),

    path("reading_mocktest", ReadingMocktestView.as_view()),
    path("reading_mocktests", ReadingMocktestListView.as_view()),
    path("reading_mocktest/<int:id>", ReadingMocktestUpdateDeleteView.as_view()),

    path("speaking_mocktest", SpeakingMocktestView.as_view()),
    path("speaking_mocktests", SpeakingMocktestListView.as_view()),
    path("speaking_mocktest/<int:id>", SpeakingMocktestUpdateDeleteView.as_view()),

    path("listening_mocktest", ListeningMocktestView.as_view()),
    path("listening_mocktests", ListeningMocktestListView.as_view()),
    path("listening_mocktest/<int:id>", ListeningMocktestUpdateDeleteView.as_view()),

    path("full_mocktest", FullMocktestView.as_view()),
    path("full_mocktests", FullMocktestListView.as_view()),
    path("full_mocktest/<int:id>", FullMocktestUpdateDeleteView.as_view()),
]