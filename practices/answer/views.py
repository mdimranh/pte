from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Answer
from .serializers import AnswerCreateSerializer, AnswerListSerializer


class AnswerListView(ListAPIView):
    serializer_class = AnswerListSerializer
    queryset = Answer.objects.all()

class AnswerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerCreateSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)