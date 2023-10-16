from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import Dictation


class DictationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictation
        fields = '__all__'

class DictationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictation
        exclude = [
            'content'
        ]

class DictationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictation
        fields = [
            "id", "title", "audio"
        ]

class DictationAnswerCreateSerializer(serializers.ModelSerializer):
    dictation = serializers.PrimaryKeyRelatedField(queryset=Dictation.objects.all())
    answer = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        model = Answer
        fields = [
            "dictation",
            "answer"
        ]

class DictationAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]