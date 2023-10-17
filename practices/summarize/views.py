from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import SummarizeSerializer
from .models import Summarize
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class SummarizeListView(ListAPIView):
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeDetailView(RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()
