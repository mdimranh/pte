from rest_framework import serializers

from accounts.serializers import UserDetailsSerializer

from .models import Plan, Purchase


class PlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "title", "description", "thumbnail", "start_date", "end_date"]

class PlanSerializer(serializers.ModelSerializer):
    available_account = serializers.SerializerMethodField()
    plan = PlanDetailsSerializer()
    student = UserDetailsSerializer(many=True)
    class Meta:
        model = Purchase
        fields = ['id', "plan", 'student', 'available_account']

    def get_available_account(self, obj):
        return obj.available_account

class PlanList(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'