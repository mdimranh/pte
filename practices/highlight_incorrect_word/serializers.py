from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import HighlightIncorrectWord


class HighlightIncorrectWordSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        options, right_options = attrs.get('options'), attrs.get('right_options')
        if options is not None and right_options is not None:
            for roption in right_options:
                found = False
                for option in options:
                    if option.get('value') == roption:
                        found = True
                if not found:
                    raise serializers.ValidationError({"right_options": ["right_options not in options"]})
        return attrs

    class Meta:
        model = HighlightIncorrectWord
        fields = '__all__'

class HighlightIncorrectWordDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightIncorrectWord
        exclude = [
            'right_options'
        ]

class HighlightIncorrectWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightIncorrectWord
        fields = [
            "id", "title", "audio", "options", "appeared", "prediction"
        ]