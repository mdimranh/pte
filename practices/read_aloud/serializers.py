from rest_framework import serializers

from .models import ReadAloud
from ..answer.models import Answer
from ..discussion.serializers import UserSerializer


class ReadAloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadAloud
        fields = [
            "id", "title", "content", "tested" 
        ]

class ReadAloudAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "read_aloud",
            "audio" 
        ]

class ReadAloudAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "scores" 
        ]