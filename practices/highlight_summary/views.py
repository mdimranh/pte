from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..discussion.views import CustomPagination
from .models import HighlightSummary
from .serializers import *


class HighlightSummaryListAPIView(ListAPIView):
    queryset = HighlightSummary.objects.all()
    serializer_class = HighlightSummaryListSerializer
    pagination_class = CustomPagination

class HighlightSummaryCreateAPIView(CreateAPIView):
    queryset = HighlightSummary.objects.all()
    serializer_class = HighlightSummarySerializer
    pagination_class = CustomPagination


class HighlightSummaryDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = HighlightSummaryDetailsSerializer
    queryset = HighlightSummary.objects.all()

class HighlightSummaryAnswerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HighlightSummaryAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            highlight_summary = serializer.validated_data.get("highlight_summary")
            score = 1 if highlight_summary.right_option == serializer.validated_data.get("answer") else 0
            serializer.save(user=self.request.user, score=score)
            return Response({
                "score": score,
                "right_option": highlight_summary.right_option
            })
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class HighlightSummaryAnswerListView(ListAPIView):
    serializer_class = HighlightSummaryAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(highlight_summary=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = HighlightSummaryAnswerListSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(highlight_summary=pk, user=self.request.user)

        return queryset