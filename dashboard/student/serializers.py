from rest_framework import serializers

from accounts.models import User

from .models import ExamCountdown, TargetScore


class ExamCountdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCountdown
        fields = ["exam_date"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'full_name', 'picture']

class ExamCountdownListSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = ExamCountdown
        fields = ["exam_date", "student"]

class TargetScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetScore
        fields = ["score"]