from django.urls import path

from .views import *

urlpatterns = [
    path('short_question', ShortQuestionCreateAPIView.as_view()),
    path('short_questions', ShortQuestionListAPIView.as_view()),
    path('short_question/<int:pk>', ShortQuestionDetailsView.as_view()),
    path('short_question/<int:pk>/answer', ShortQuestionAnswerListView.as_view()),
    # path('short_question/answer', ShortQuestionAnswerCreateView.as_view()),
    path('short_question/<int:pk>/my_answer', MyAnswerListView.as_view())
]