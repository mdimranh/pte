from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.security.permission import IsStudentPermission
from ..discussion.views import CustomPagination
from .models import Dictation
from .serializers import *


class DictationListAPIView(ListAPIView):
    queryset = Dictation.objects.all()
    serializer_class = DictationListSerializer
    pagination_class = CustomPagination

class DictationCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Dictation.objects.all()
    serializer_class = DictationSerializer

class DictationUpdateAPIView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = [IsAdminUser]
    queryset = Dictation.objects.all()
    serializer_class = DictationSerializer

class DictationDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = DictationDetailsSerializer
    queryset = Dictation.objects.all()


import difflib


def get_score(self, sentence1, sentence2):
        words1 = sentence1.split()
        words2 = sentence2.split()

        # Calculate the difference between the two sentences
        differ = difflib.Differ()
        diff = list(differ.compare(words1, words2))

        result, words = {}, []
        # Process the difference
        score = 0
        for word_diff in diff:
            word = word_diff[2:]
            if word_diff.startswith('  '):  # Matched words
                words.append({word: "correct"})
                score += 1
            elif word_diff.startswith('- '):  # Words missing in sentence2
                words.append({word: "missed"})
            elif word_diff.startswith('+ '):  # Words wrong in sentence2
                words.append({word: "wrong"})

        result['score'] = score
        result['words'] = words
        return result

class DictationAnswerCreateView(APIView):
    permission_classes = [IsStudentPermission]
        
    def post(self, request):
        serializer = DictationAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            score = get_score(serializer.validated_data['dictation'].content, serializer.validated_data['answer'])
            serializer.save(user=self.request.user, score=score.get('score'))
            return Response({
                "score": score.get('score'),
                "detail_answer": score.get('words'),
                "max_score": len(serializer.validated_data['dictation'].content.split(" "))
            })
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class DictationAnswerListView(ListAPIView):
    serializer_class = DictationAnswerListSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Answer.objects.filter(dictation=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = DictationAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(dictation=pk, user=self.request.user)

        return queryset