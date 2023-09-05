from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import HighlightSummary


class HighlightSummarySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('right_option') is not None and attrs.get('options') is not None:
            if  attrs.get('right_option') not in attrs.get('options'):
                raise serializers.ValidationError({"right_option": ["right_option not in options"]})
        return attrs

    class Meta:
        model = HighlightSummary
        fields = '__all__'

class HighlightSummaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightSummary
        exclude = [
            'right_option'
        ]

class HighlightSummaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightSummary
        fields = [
            "id", "title", "audio", "options"
        ]

class HighlightSummaryAnswerCreateSerializer(serializers.ModelSerializer):
    highlight_summary = serializers.PrimaryKeyRelatedField(queryset=HighlightSummary.objects.all())
    answer = serializers.CharField(allow_blank=False, required=True)

    def validate(self, data):
        if data.get('answer') not in data.get('highlight_summary').options:
            raise serializers.ValidationError({"answer": ["Not in options"]})
        return data

    class Meta:
        model = Answer
        fields = [
            "highlight_summary",
            "answer"
        ]

class HighlightSummaryAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score"
        ]