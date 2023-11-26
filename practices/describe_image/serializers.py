from rest_framework import serializers

from ..answer.models import Answer
from ..discussion.serializers import UserSerializer
from .models import DescribeImage


class DescribeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeImage
        fields = '__all__'

class DescribeImageDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeImage
        fields = '__all__'

class DescribeImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeImage
        fields = [
            "id", "title", "image", "reference_text", "prediction", "appeared"
        ]

# class DescribeImageAnswerCreateSerializer(serializers.ModelSerializer):
#     highlight_summary = serializers.PrimaryKeyRelatedField(queryset=DescribeImage.objects.all())
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

class DescribeImageAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]