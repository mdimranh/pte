from django.urls import path

from .views import *

urlpatterns = [
    path('write_easy', WriteEasyCreateAPIView.as_view()),
    path('write_easy/<int:id>/update', WriteEasyUpdateAPIView.as_view()),
    path('write_easies', WriteEasyListAPIView.as_view()),
    path('write_easy/<int:pk>', WriteEasyDetailsView.as_view()),
    path('write_easy/<int:pk>/answer', WriteEasyAnswerListView.as_view()),
    # path('write_easy/answer', WriteEasyAnswerCreateView.as_view()),
    path('write_easy/<int:pk>/my_answer', MyAnswerListView.as_view())
]