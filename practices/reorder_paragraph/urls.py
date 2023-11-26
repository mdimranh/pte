from django.urls import path

from .views import *

urlpatterns = [
    path('reorder_paragraph', ReorderParagraphCreateAPIView.as_view()),
    path('reorder_paragraph/<int:id>/update', ReorderParagraphUpdateAPIView.as_view()),
    path('reorder_paragraphs', ReorderParagraphListAPIView.as_view()),
    path('reorder_paragraph/<int:pk>', ReorderParagraphDetailsView.as_view()),
    path('reorder_paragraph/<int:pk>/answer', ReorderParagraphAnswerListView.as_view()),
    # path('reorder_paragraph/answer', ReorderParagraphAnswerCreateView.as_view()),
    path('reorder_paragraph/<int:pk>/my_answer', MyAnswerListView.as_view())
]