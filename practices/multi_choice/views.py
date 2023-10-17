from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.security.permission import IsStudentPermission
from ..discussion.views import CustomPagination
from .models import MultiChoice
from .serializers import *


class MultiChoiceListAPIView(ListAPIView):
    queryset = MultiChoice.objects.filter(single=False)
    serializer_class = MultiChoiceListSerializer
    pagination_class = CustomPagination

class MultiChoiceSingleanswerListAPIView(ListAPIView):
    queryset = MultiChoice.objects.filter(single=True)
    serializer_class = MultiChoiceListSerializer
    pagination_class = CustomPagination

class MultiChoiceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = MultiChoice.objects.all()
    serializer_class = MultiChoiceSerializer
    pagination_class = CustomPagination


class MultiChoiceDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = MultiChoiceDetailsSerializer
    queryset = MultiChoice.objects.all()

class MultiChoiceAnswerCreateView(APIView):
    permission_classes = [IsStudentPermission]

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
        serializer = MultiChoiceAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            score = self.calculate_score(serializer.validated_data['answers'], serializer.validated_data['multi_choice'].right_options)
            serializer.save(user=self.request.user, score=score)
            return Response({
                # "score": round(score * len(serializer.validated_data['multi_choice'].options), 2),
                "score": score,
                "right_options": serializer.validated_data['multi_choice'].right_options,
                "wrong_answers": [answer for answer in serializer.validated_data['answers'] if answer not in serializer.validated_data['multi_choice'].right_options],
                "max_score": len(serializer.validated_data['multi_choice'].right_options)
            })
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class MultiChoiceAnswerListView(ListAPIView):
    serializer_class = MultiChoiceAnswerListSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Answer.objects.filter(multi_choice=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = MultiChoiceAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(multi_choice=pk, user=self.request.user)

        return queryset