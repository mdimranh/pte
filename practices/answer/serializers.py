from rest_framework import serializers

from ..discussion.serializers import UserSerializer
from .models import Answer
from ..summarize.models import Summarize


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


class SummarizeAnswerSerializer(serializers.ModelSerializer):
    summarize = serializers.PrimaryKeyRelatedField(queryset=Summarize.objects.all())
    summarize_text = serializers.CharField()
    class Meta:
        model = Answer
        fields = [
            "summarize",
            "summarize_text"
        ]

class SummarizeAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "scores"
        ]