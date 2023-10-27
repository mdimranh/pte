from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import WriteEasy
from .serializers import *


class WriteEasyListAPIView(ListAPIView):
    queryset = WriteEasy.objects.all()
    serializer_class = WriteEasyListSerializer
    pagination_class = CustomPagination

class WriteEasyCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = WriteEasy.objects.all()
    serializer_class = WriteEasySerializer
    pagination_class = CustomPagination


class WriteEasyDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = WriteEasyDetailsSerializer
    queryset = WriteEasy.objects.all()

# class WriteEasyAnswerCreateView(APIView):
#     permission_classes = [IsStudentPermission]

#     def post(self, request):
#         serializer = WriteEasyAnswerCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             write_easy = serializer.validated_data.get("write_easy")
#             score = 1 if write_easy.right_option == serializer.validated_data.get("answer") else 0
#             serializer.save(user=self.request.user, score=score)
#             return Response({
#                 "score": score,
#                 "right_option": write_easy.right_option,
#                 "max_score": 1
#             })
#         else:
#             return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class WriteEasyAnswerListView(ListAPIView):
    serializer_class = WriteEasyAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(write_easy=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = WriteEasyAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(write_easy=pk, user=self.request.user)

        return queryset