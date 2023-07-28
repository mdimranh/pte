from rest_framework.generics import ListAPIView

from .models import Answer
from .serializers import AnswerListSerializer


class AnswerListView(ListAPIView):
    serializer_class = AnswerListSerializer
    queryset = Answer.objects.all()