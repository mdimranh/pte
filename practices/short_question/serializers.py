from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import ShortQuestion


class ShortQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestion
        fields = '__all__'

class ShortQuestionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestion
        fields = '__all__'

class ShortQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestion
        fields = [
            "id", "title", "audio", "reference_text"
        ]

# class ShortQuestionAnswerCreateSerializer(serializers.ModelSerializer):
#     highlight_summary = serializers.PrimaryKeyRelatedField(queryset=ShortQuestion.objects.all())
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

class ShortQuestionAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]