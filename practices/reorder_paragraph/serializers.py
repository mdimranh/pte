from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import ReorderParagraph


class ReorderParagraphSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        options, answer_sequence = attrs.get('options'), attrs.get('answer_sequence')
        if options is not None and answer_sequence is not None:
            for roption in answer_sequence:
                found = False
                for option in options:
                    if option.get('index') == roption:
                        found = True
                if not found:
                    raise serializers.ValidationError({"answer_sequence": ["answer_sequence not in options"]})
        return attrs

    class Meta:
        model = ReorderParagraph
        fields = '__all__'

class ReorderParagraphDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderParagraph
        exclude = [
            'answer_sequence'
        ]

class ReorderParagraphListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderParagraph
        fields = [
            "id", "title", "paragraph", "options", "prediction", "appeared"
        ]

class ReorderParagraphAnswerCreateSerializer(serializers.ModelSerializer):
    reorder_paragraph = serializers.PrimaryKeyRelatedField(queryset=ReorderParagraph.objects.all())
    answers = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        options = [option.get('index') for option in data.get('reorder_paragraph').options]
        for answer in data.get('answers'):
            if answer not in options:
                raise serializers.ValidationError({"answers": ["Not in options"]})
        return data

    class Meta:
        model = Answer
        fields = [
            "reorder_paragraph",
            "answers"
        ]

class ReorderParagraphAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]