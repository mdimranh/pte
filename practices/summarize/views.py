from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import SummarizeSerializer
from .models import Summarize


class SummarizeListView(ListAPIView):
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeCreateView(CreateAPIView):
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeDetailView(RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()
