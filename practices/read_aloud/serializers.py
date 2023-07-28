from rest_framework import serializers

from .models import ReadAloud


class ReadAloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadAloud
        fields = [
            "title", "article", "tested" 
        ]