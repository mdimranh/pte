from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import WriteEasy


class WriteEasySerializer(serializers.ModelSerializer):
    class Meta:
        model = WriteEasy
        fields = '__all__'

class WriteEasyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriteEasy
        fields = '__all__'

class WriteEasyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriteEasy
        fields = [
            "id", "title", "question", "reference_text"
        ]

# class WriteEasyAnswerCreateSerializer(serializers.ModelSerializer):
#     highlight_summary = serializers.PrimaryKeyRelatedField(queryset=WriteEasy.objects.all())
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

class WriteEasyAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]