from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.security.permission import IsStudentPermission

from ..discussion.views import CustomPagination
from .models import RetellSentence
from .serializers import *


class RetellSentenceListAPIView(ListAPIView):
    queryset = RetellSentence.objects.all()
    serializer_class = RetellSentenceListSerializer
    pagination_class = CustomPagination

class RetellSentenceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = RetellSentence.objects.all()
    serializer_class = RetellSentenceSerializer

class RetellSentenceUpdateAPIView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = RetellSentence.objects.all()
    serializer_class = RetellSentenceSerializer

class RetellSentenceDetailsView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = RetellSentenceDetailsSerializer
    queryset = RetellSentence.objects.all()

# class RetellSentenceAnswerCreateView(APIView):
#     permission_classes = [IsStudentPermission]

#     def post(self, request):
#         serializer = RetellSentenceAnswerCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             retell_sentence = serializer.validated_data.get("retell_sentence")
#             score = 1 if retell_sentence.right_option == serializer.validated_data.get("answer") else 0
#             serializer.save(user=self.request.user, score=score)
#             return Response({
#                 "score": score,
#                 "right_option": retell_sentence.right_option,
#                 "max_score": 1
#             })
#         else:
#             return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class RetellSentenceAnswerListView(ListAPIView):
    serializer_class = RetellSentenceAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(retell_sentence=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = RetellSentenceAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(retell_sentence=pk, user=self.request.user)

        return queryset