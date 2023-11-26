from rest_framework import serializers
from .models import Blank, RWBlank, ReadingBlank
from ..answer.models import Answer
from ..discussion.serializers import UserSerializer

class BlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = '__all__'

class BlankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = [
            "id", "title", "sentence", "appeared", "prediction"
        ]

class BlankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = [
            "id", "title", "appeared", "prediction"
        ]

class BlankAnswerCreateSerializer(serializers.ModelSerializer):
    blank = serializers.PrimaryKeyRelatedField(queryset=Blank.objects.all())
    answers = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Answer
        fields = [
            "blank",
            "answers"
        ]

class BlankAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Answer
        fields = [
            "user",
            "score",
            "max_score",
            "created_at"
        ]


# RWBlank
class RWBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = RWBlank
        # exclude = ['options']
        fields = '__all__'

class RWBlankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RWBlank
        fields = [
            "id", "title", "sentence", "option_list", "appeared", "prediction"
        ]

class RWBlankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RWBlank
        fields = [
            "id", "title", "appeared", "prediction"
        ]


# Reading Blank

class ReadingBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBlank
        fields = '__all__'

class ReadingBlankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBlank
        fields = [
            "id", "title", "sentence", "appeared", "prediction"
        ]

class ReadingBlankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBlank
        fields = [
            "id", "title", "appeared", "prediction"
        ]