from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import HighlightIncorrectWord
from .serializers import *


class HighlightIncorrectWordListAPIView(ListAPIView):
    queryset = HighlightIncorrectWord.objects.filter()
    serializer_class = HighlightIncorrectWordListSerializer
    pagination_class = CustomPagination

class HighlightIncorrectWordCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = HighlightIncorrectWord.objects.all()
    serializer_class = HighlightIncorrectWordSerializer

class HighlightIncorrectWordUpdateAPIView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = HighlightIncorrectWord.objects.all()
    serializer_class = HighlightIncorrectWordSerializer

class HighlightIncorrectWordDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = HighlightIncorrectWordDetailsSerializer
    queryset = HighlightIncorrectWord.objects.all()