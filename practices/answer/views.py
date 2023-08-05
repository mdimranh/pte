from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Answer
from .serializers import AnswerCreateSerializer, AnswerListSerializer, SummarizeAnswerListSerializer


class AnswerListView(ListAPIView):
    serializer_class = AnswerListSerializer
    queryset = Answer.objects.all()

class AnswerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerCreateSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SummarizeAnswerListView(ListAPIView):
    serializer_class = SummarizeAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(summarize=pk)

        return queryset