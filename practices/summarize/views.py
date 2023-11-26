from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import SummarizeSerializer, SummarizeSpokenSerializer
from .models import Summarize, SummarizeSpoken
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class SummarizeListView(ListAPIView):
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeUpdateView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()

class SummarizeDetailView(RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SummarizeSerializer
    queryset = Summarize.objects.all()


class SummarizeSpokenListView(ListAPIView):
    serializer_class = SummarizeSpokenSerializer
    queryset = SummarizeSpoken.objects.all()

class SummarizeSpokenCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SummarizeSpokenSerializer
    queryset = SummarizeSpoken.objects.all()

class SummarizeSpokenUpdateView(UpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    serializer_class = SummarizeSpokenSerializer
    queryset = SummarizeSpoken.objects.all()

class SummarizeSpokenDetailView(RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SummarizeSpokenSerializer
    queryset = SummarizeSpoken.objects.all()
