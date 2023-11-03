from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import MultiChoice


class MultiChoiceSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('right_options') is not None and attrs.get('options') is not None:
            for option in attrs.get('right_options'):
                if  option not in attrs.get('options'):
                    raise serializers.ValidationError({"right_options": ["right_options not in options"]})
        return attrs

    class Meta:
        model = MultiChoice
        fields = '__all__'

class MultiChoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        exclude = [
            'right_options'
        ]

class MultiChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        fields = [
            "id", "title", "audio", "options", "appeared", "prediction"
        ]

class MultiChoiceAnswerCreateSerializer(serializers.ModelSerializer):
    multi_choice = serializers.PrimaryKeyRelatedField(queryset=MultiChoice.objects.all())
    answers = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        for answer in data.get('answers'):
            if answer not in data.get('multi_choice').options:
                raise serializers.ValidationError({"answers": ["Not in options"]})
        return data

    class Meta:
        model = Answer
        fields = [
            "multi_choice",
            "answers"
        ]

class MultiChoiceAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]