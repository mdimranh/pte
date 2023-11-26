from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import ShortQuestion
from .serializers import *


class ShortQuestionListAPIView(ListAPIView):
    queryset = ShortQuestion.objects.all()
    serializer_class = ShortQuestionListSerializer
    pagination_class = CustomPagination

class ShortQuestionCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ShortQuestion.objects.all()
    serializer_class = ShortQuestionSerializer

class ShortQuestionUpdateAPIView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = ShortQuestion.objects.all()
    serializer_class = ShortQuestionSerializer

class ShortQuestionDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = ShortQuestionDetailsSerializer
    queryset = ShortQuestion.objects.all()

# class ShortQuestionAnswerCreateView(APIView):
#     permission_classes = [IsStudentPermission]

#     def post(self, request):
#         serializer = ShortQuestionAnswerCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             repeat_sentence = serializer.validated_data.get("repeat_sentence")
#             score = 1 if repeat_sentence.right_option == serializer.validated_data.get("answer") else 0
#             serializer.save(user=self.request.user, score=score)
#             return Response({
#                 "score": score,
#                 "right_option": repeat_sentence.right_option,
#                 "max_score": 1
#             })
#         else:
#             return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ShortQuestionAnswerListView(ListAPIView):
    serializer_class = ShortQuestionAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(repeat_sentence=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = ShortQuestionAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(repeat_sentence=pk, user=self.request.user)

        return queryset