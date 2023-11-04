from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import DescribeImage
from .serializers import *


class DescribeImageListAPIView(ListAPIView):
    queryset = DescribeImage.objects.all()
    serializer_class = DescribeImageListSerializer
    pagination_class = CustomPagination

class DescribeImageCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = DescribeImage.objects.all()
    serializer_class = DescribeImageSerializer
    pagination_class = CustomPagination


class DescribeImageDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = DescribeImageDetailsSerializer
    queryset = DescribeImage.objects.all()

# class DescribeImageAnswerCreateView(APIView):
#     permission_classes = [IsStudentPermission]

#     def post(self, request):
#         serializer = DescribeImageAnswerCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             describe_image = serializer.validated_data.get("describe_image")
#             score = 1 if describe_image.right_option == serializer.validated_data.get("answer") else 0
#             serializer.save(user=self.request.user, score=score)
#             return Response({
#                 "score": score,
#                 "right_option": describe_image.right_option,
#                 "max_score": 1
#             })
#         else:
#             return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class DescribeImageAnswerListView(ListAPIView):
    serializer_class = DescribeImageAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(describe_image=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = DescribeImageAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(describe_image=pk, user=self.request.user)

        return queryset