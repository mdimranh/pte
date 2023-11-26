from rest_framework import generics
from .models import *
from .serializers import *

class WrittingMocktestView(generics.CreateAPIView):
    queryset = WrittingMocktest.objects.all()
    serializer_class = WrittingMocktestSerializer

class WrittingMocktestListView(generics.ListAPIView):
    queryset = WrittingMocktest.objects.all()
    serializer_class = WrittingMocktestSerializer

class WrittingMocktestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = WrittingMocktestSerializer
    queryset = WrittingMocktest.objects.all()




class ReadingMocktestView(generics.CreateAPIView):
    queryset = ReadingMocktest.objects.all()
    serializer_class = ReadingMocktestSerializer

class ReadingMocktestListView(generics.ListAPIView):
    queryset = ReadingMocktest.objects.all()
    serializer_class = ReadingMocktestSerializer

class ReadingMocktestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = ReadingMocktestSerializer
    queryset = ReadingMocktest.objects.all()




class SpeakingMocktestView(generics.CreateAPIView):
    queryset = SpeakingMocktest.objects.all()
    serializer_class = SpeakingMocktestSerializer

class SpeakingMocktestListView(generics.ListAPIView):
    queryset = SpeakingMocktest.objects.all()
    serializer_class = SpeakingMocktestSerializer

class SpeakingMocktestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = SpeakingMocktestSerializer
    queryset = SpeakingMocktest.objects.all()




class ListeningMocktestView(generics.CreateAPIView):
    queryset = ListeningMocktest.objects.all()
    serializer_class = ListeningMocktestSerializer

class ListeningMocktestListView(generics.ListAPIView):
    queryset = ListeningMocktest.objects.all()
    serializer_class = ListeningMocktestSerializer

class ListeningMocktestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = ListeningMocktestSerializer
    queryset = ListeningMocktest.objects.all()





class FullMocktestView(generics.CreateAPIView):
    queryset = FullMocktest.objects.all()
    serializer_class = FullMocktestSerializer

class FullMocktestListView(generics.ListAPIView):
    queryset = FullMocktest.objects.all()
    serializer_class = FullMocktestSerializer

class FullMocktestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = FullMocktestSerializer
    queryset = FullMocktest.objects.all()