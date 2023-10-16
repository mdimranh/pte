from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import MissingWord


class MissingWordSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('right_options') is not None and attrs.get('options') is not None:
            for option in attrs.get('right_options'):
                if  option not in attrs.get('options'):
                    raise serializers.ValidationError({"right_options": ["right_options not in options"]})
        return attrs

    class Meta:
        model = MissingWord
        fields = '__all__'

class MissingWordDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingWord
        exclude = [
            'right_options'
        ]

class MissingWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingWord
        fields = [
            "id", "title", "audio", "options"
        ]

class MissingWordAnswerCreateSerializer(serializers.ModelSerializer):
    missing_word = serializers.PrimaryKeyRelatedField(queryset=MissingWord.objects.all())
    answers = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        for answer in data.get('answers'):
            if answer not in data.get('missing_word').options:
                raise serializers.ValidationError({"answers": ["Not in options"]})
        return data

    class Meta:
        model = Answer
        fields = [
            "missing_word",
            "answers"
        ]

class MissingWordAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]