from rest_framework import serializers
from .models import *

class WrittingMocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittingMocktest
        fields = '__all__'

class ReadingMocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingMocktest
        fields = '__all__'

class SpeakingMocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingMocktest
        fields = '__all__'

class ListeningMocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningMocktest
        fields = '__all__'

class FullMocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullMocktest
        fields = '__all__'