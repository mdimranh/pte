from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..discussion.views import CustomPagination
from .models import MissingWord
from .serializers import *


class MissingWordListAPIView(ListAPIView):
    queryset = MissingWord.objects.all()
    serializer_class = MissingWordListSerializer
    pagination_class = CustomPagination

class MissingWordCreateAPIView(CreateAPIView):
    queryset = MissingWord.objects.all()
    serializer_class = MissingWordSerializer
    pagination_class = CustomPagination


class MissingWordDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = MissingWordDetailsSerializer
    queryset = MissingWord.objects.all()

class MissingWordAnswerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_score(self, correct_answers, selected_answers, incorrect_penalty=1):
        score = 0
        base_score = len(correct_answers)
        for selected_answer in selected_answers:
            if selected_answer in correct_answers:
                score += 1
            else:
                score -= incorrect_penalty
        for answer in correct_answers:
            if answer not in selected_answers:
                score -= 1

        return max(score, 0)
        
    def post(self, request):
        serializer = MissingWordAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            score = self.calculate_score(serializer.validated_data['answers'], serializer.validated_data['missing_word'].right_options)
            serializer.save(user=self.request.user, score=score)
            return Response({
                "score": score,
                "right_options": serializer.validated_data['missing_word'].right_options,
                "wrong_answers": [answer for answer in serializer.validated_data['answers'] if answer not in serializer.validated_data['missing_word'].right_options]
            })
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class MissingWordAnswerListView(ListAPIView):
    serializer_class = MissingWordAnswerListSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Answer.objects.filter(missing_word=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = MissingWordAnswerListSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(missing_word=pk, user=self.request.user)

        return queryset