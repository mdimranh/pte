from django.urls import path

from .views import *

urlpatterns = [
    path('multi_choice', MultiChoiceCreateAPIView.as_view()),
    path('multi_choices', MultiChoiceListAPIView.as_view()),
    path('multi_choices/single-answer', MultiChoiceSingleanswerListAPIView.as_view()),
    path('multi_choice/<int:pk>', MultiChoiceDetailsView.as_view()),
    path('multi_choice/<int:pk>/answer', MultiChoiceAnswerListView.as_view()),
    path('multi_choice/answer', MultiChoiceAnswerCreateView.as_view()),
    path('multi_choice/<int:pk>/my_answer', MyAnswerListView.as_view())
]