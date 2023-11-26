from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import RepeatSentence


class RepeatSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatSentence
        fields = '__all__'

class RepeatSentenceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatSentence
        fields = '__all__'

class RepeatSentenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatSentence
        fields = [
            "id", "title", "audio", "reference_text"
        ]

# class RepeatSentenceAnswerCreateSerializer(serializers.ModelSerializer):
#     highlight_summary = serializers.PrimaryKeyRelatedField(queryset=RepeatSentence.objects.all())
#     answer = serializers.CharField(allow_blank=False, required=True)

#     def validate(self, data):
#         if data.get('answer') not in data.get('highlight_summary').options:
#             raise serializers.ValidationError({"answer": ["Not in options"]})
#         return data

#     class Meta:
#         model = Answer
#         fields = [
#             "highlight_summary",
#             "answer"
#         ]

class RepeatSentenceAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]