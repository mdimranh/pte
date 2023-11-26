from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import RetellSentence


class RetellSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetellSentence
        fields = '__all__'

class RetellSentenceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetellSentence
        fields = '__all__'

class RetellSentenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetellSentence
        fields = [
            "id", "title", "audio", "reference_text"
        ]

# class RetellSentenceAnswerCreateSerializer(serializers.ModelSerializer):
#     highlight_summary = serializers.PrimaryKeyRelatedField(queryset=RetellSentence.objects.all())
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

class RetellSentenceAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]