from rest_framework import serializers
from management.models import Plan

class PaymentSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(max_length=20)
    plan = serializers.ModelField(model_field=Plan)
