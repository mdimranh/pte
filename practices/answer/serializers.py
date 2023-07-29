from rest_framework import serializers

from ..discussion.serializers import UserSerializer
from .models import Answer


class AnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "audio",
            'user',
            "score",
            "scores"
        ]

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["read_aloud", "audio"]