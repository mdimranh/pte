from django.urls import path

from .views import *

urlpatterns = [
    path('multi_choice', MultiChoiceCreateAPIView.as_view()),
    path('multi_choice/<int:id>/update', MultiChoiceUpdateAPIView.as_view()),
    path('multi_choices', MultiChoiceListAPIView.as_view()),
    path('multi_choices/single-answer', MultiChoiceSingleanswerListAPIView.as_view()),
    path('multi_choice/<int:pk>', MultiChoiceDetailsView.as_view()),
    path('multi_choice/<int:pk>/answer', MultiChoiceAnswerListView.as_view()),
    path('multi_choice/answer', MultiChoiceAnswerCreateView.as_view()),
    path('multi_choice/<int:pk>/my_answer', MyAnswerListView.as_view()),
    #* reading
    path('multi_choice/reading', MultiChoiceReadingCreateAPIView.as_view()),
    path('multi_choice/reading/<int:id>/update', MultiChoiceReadingUpdateAPIView.as_view()),
    path('multi_choices/reading', MultiChoiceReadingListAPIView.as_view()),
    path('multi_choices/reading/single-answer', MultiChoiceReadingSingleanswerListAPIView.as_view()),
    path('multi_choice/reading/<int:pk>', MultiChoiceReadingDetailsView.as_view()),
    path('multi_choice/reading/<int:pk>/answer', MultiChoiceReadingAnswerListView.as_view()),
    path('multi_choice/reading/answer', MultiChoiceReadingAnswerCreateView.as_view()),
    path('multi_choice/reading/<int:pk>/my_answer', MyReadingAnswerListView.as_view())
]