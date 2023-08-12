from rest_framework import serializers
from .models import Summarize

class SummarizeSerializer(serializers.ModelSerializer):
    self_bookmark = serializers.SerializerMethodField()
    class Meta:
        model = Summarize
        fields = [
            "id", "title", "content", "practiced", "self_bookmark", "prediction", "appeared"
        ]

    def get_self_bookmark(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmark.filter(id=request.user.id).exists()
        else:
            return False