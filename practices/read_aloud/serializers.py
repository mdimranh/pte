from rest_framework import serializers

from .models import ReadAloud
from ..answer.models import Answer
from ..discussion.serializers import UserSerializer


class ReadAloudSerializer(serializers.ModelSerializer):
    self_bookmark = serializers.SerializerMethodField()
    class Meta:
        model = ReadAloud
        fields = [
            "id", "title", "content", "practiced", "self_bookmark"
        ]

    def get_self_bookmark(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmark.filter(id=request.user.id).exists()
        else:
            return False

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