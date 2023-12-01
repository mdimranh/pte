from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import MultiChoice, MultiChoiceReading


class MultiChoiceSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('single', False):
            if len(attrs.get('right_options')) != 1:
                raise serializers.ValidationError({"right_options": ["right_options length must be 1"]})
        options, right_options = attrs.get('options'), attrs.get('right_options')
        available_options = [option.get('value') for option in options]
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
        options = [option.get('value') for option in data.get('multi_choice').options]
        for answer in data.get('answers'):
            if answer not in options:
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

# reading

class MultiChoiceReadingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('single', False):
            if len(attrs.get('right_options')) != 1:
                raise serializers.ValidationError({"right_options": ["right_options length must be 1"]})
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
        model = MultiChoiceReading
        fields = '__all__'

class MultiChoiceReadingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoiceReading
        exclude = [
            'right_options'
        ]

class MultiChoiceReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoiceReading
        fields = [
            "id", "title", "content", "options", "appeared", "prediction"
        ]

class MultiChoiceReadingAnswerCreateSerializer(serializers.ModelSerializer):
    multi_choice = serializers.PrimaryKeyRelatedField(queryset=MultiChoiceReading.objects.all())
    answers = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        options = [option.get('value') for option in data.get('multi_choice').options]
        for answer in data.get('answers'):
            if answer not in options:
                raise serializers.ValidationError({"answers": ["Not in options"]})
        return data

    class Meta:
        model = Answer
        fields = [
            "multi_choice_reading",
            "answers"
        ]

class MultiChoiceReadingAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]