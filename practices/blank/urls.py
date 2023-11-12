from django.urls import path

from .views import *

urlpatterns = [
    path('blank', BlankCreateAPIView.as_view()),
    path('blanks', BlankListAPIView.as_view()),
    path('blank/<int:pk>', BlankDetailsView.as_view()),
    path('blank/<int:pk>/answer', BlankAnswerListView.as_view()),
    path('blank/answer', BlankAnswerCreateView.as_view()),
    path('blank/<int:pk>/my_answer', MyAnswerListView.as_view()),
    #RWBlank
    path('read-write/blank', RWBlankCreateAPIView.as_view()),
    path('read-write/blanks', RWBlankListAPIView.as_view()),
    path('read-write/blank/<int:pk>', RWBlankDetailsView.as_view()),
]