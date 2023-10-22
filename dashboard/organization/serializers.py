from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts.models import User
from management.models import Group, Plan, Profile, Purchase
from management.serializers import PlanSerializer


class CreateStudentSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    email = serializers.EmailField()
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    group = serializers.CharField()


    def create(self, validated_data):
        user_data = {
            'is_student': True,
            'password': validated_data.get('password'),
            "full_name": validated_data.get('full_name')
        }
        if 'email' in validated_data:
            user_data['email'] = validated_data['email']
        user = User.objects.create_user(**user_data)
        user.set_password(validated_data['password'])
        profile, create = Profile.objects.get_or_create(
            user=user
        )
        profile.userid = validated_data['userid']
        profile.plan = validated_data['plan']
        profile.organization = self.context['request'].user
        if 'group' in validated_data:
            profile.group = validated_data['group']
        profile.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user", 'id']

class StudentListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    premium = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'picture', 'last_login','profile', 'premium']

    def get_premium(self, obj):
        return Purchase.objects.filter(student=obj.pk).exists()

class ProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields=['title', 'description', 'start_date', 'end_date', 'thumbnail']

class StudentDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileDetailsSerializer(many=True)
    plans = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone", "picture", "profile", "plans"]

    def get_plans(self, obj):
        plans_queryset = Purchase.objects.filter(student=obj).values('id')
        plans = Plan.objects.filter(id__in=plans_queryset)
        serializer = PurchaseSerializer(data=plans, many=True)
        serializer.is_valid()
        return serializer.data


class AssignPlanSerializer(serializers.Serializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_student=True))

class ChangePasswordSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_student=True))
    my_password = serializers.CharField()
    new_password = serializers.CharField()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', "organization"]