from rest_framework import serializers

from accounts.serializers import UserDetailsSerializer

from .models import Plan, Purchase, OrganizationPackage, StudentPackage


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


class OrganizationPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationPackage
        fields = '__all__'

    def save(self, **kwargs):
        validated_data = self.validated_data
        if "validation" in validated_data:
            i = 1
            for item in validated_data['validation']:
                item['id'] = i
                i+=1
        instance = super(OrganizationPackageSerializer, self).save(**validated_data, **kwargs)
        return instance

class StudentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPackage
        fields = '__all__'