from django.urls import path

from .views import *

urlpatterns = [
    path('describe_image', DescribeImageCreateAPIView.as_view()),
    path('describe_images', DescribeImageListAPIView.as_view()),
    path('describe_image/<int:pk>', DescribeImageDetailsView.as_view()),
    path('describe_image/<int:pk>/answer', DescribeImageAnswerListView.as_view()),
    # path('describe_image/answer', DescribeImageAnswerCreateView.as_view()),
    path('describe_image/<int:pk>/my_answer', MyAnswerListView.as_view())
]