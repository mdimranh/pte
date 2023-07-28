from django.urls import path

from .views import AnswerListView

urlpatterns = [
    path("answers", AnswerListView.as_view())
]