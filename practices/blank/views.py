from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import Blank, RWBlank, ReadingBlank
from .serializers import *


class BlankListAPIView(ListAPIView):
    queryset = Blank.objects.filter()
    serializer_class = BlankListSerializer
    pagination_class = CustomPagination

class BlankCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Blank.objects.all()
    serializer_class = BlankSerializer

class BlankUpdateAPIView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = [IsAdminUser]
    queryset = Blank.objects.all()
    serializer_class = BlankSerializer

class BlankDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = BlankDetailsSerializer
    queryset = Blank.objects.all()

class BlankAnswerCreateView(APIView):
    permission_classes = [IsStudentPermission]

    def calculate_score(self, correct_answers, selected_answers, incorrect_penalty=1):
        score = len(correct_answers) - len(selected_answers)
        for x in list(zip(correct_answers, selected_answers)):
            if x[0] == x[1]:
                score += 1
            else:
                score -= 1
        return max(score, 0)
        
    def post(self, request):
        serializer = BlankAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            score = self.calculate_score(serializer.validated_data['answers'], [answer.get('value') for answer in serializer.validated_data['blank'].answers])
            serializer.save(user=self.request.user, score=score)
            return Response({
                # "score": round(score * len(serializer.validated_data['blank'].options), 2),
                "score": score,
                "answers": serializer.validated_data['blank'].answers,
                "max_score": len(serializer.validated_data['blank'].answers)
            })
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class BlankAnswerListView(ListAPIView):
    serializer_class = BlankAnswerListSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Answer.objects.filter(blank=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = BlankAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(blank=pk, user=self.request.user)

        return queryset


# Reading Blank

class ReadingBlankListAPIView(ListAPIView):
    queryset = ReadingBlank.objects.filter()
    serializer_class = ReadingBlankListSerializer
    pagination_class = CustomPagination

class ReadingBlankCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ReadingBlank.objects.all()
    serializer_class = ReadingBlankSerializer


class ReadingBlankUpdateAPIView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = [IsAdminUser]
    queryset = ReadingBlank.objects.all()
    serializer_class = ReadingBlankSerializer


class ReadingBlankDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = ReadingBlankDetailsSerializer
    queryset = ReadingBlank.objects.all()

# RWBlank

class RWBlankListAPIView(ListAPIView):
    queryset = RWBlank.objects.filter()
    serializer_class = RWBlankListSerializer
    pagination_class = CustomPagination

class RWBlankCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = RWBlank.objects.all()
    serializer_class = RWBlankSerializer
    pagination_class = CustomPagination

class RWBlankUpdateAPIView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = RWBlank.objects.all()
    serializer_class = RWBlankSerializer
    pagination_class = CustomPagination


class RWBlankDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = RWBlankDetailsSerializer
    queryset = RWBlank.objects.all()