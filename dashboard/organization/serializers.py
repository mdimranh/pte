from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.response import Response

from accounts.models import User
from management.models import Group, Plan, Profile, Purchase
from management.serializers import PlanSerializer


class CreateStudentSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    email = serializers.EmailField()
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), required=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    organization = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_organization=True), required=False)

    def create(self, validated_data):
        with transaction.atomic():
            current_user = self.context.get("request").user
            user_data = {
                'is_student': True,
                'password': validated_data.get('password'),
                "full_name": validated_data.get('full_name')
            }
            if 'email' in validated_data:
                user_data['email'] = validated_data['email']
            user = User.objects.create_user(**user_data)
            user.set_password(validated_data['password'])
            user.save()
            profile, create = Profile.objects.get_or_create(
                user=user
            )
            profile.userid = validated_data['userid']
            profile.plan = validated_data['plan']
            if current_user.is_organization:
                profile.organization = self.context['request'].user
            else:
                if 'organization' in validated_data:
                    profile.organization = validated_data['organization']
            if 'group' in validated_data:
                profile.group = validated_data['group']
            profile.save()
            return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "full_name"]

class ProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    organization = OrganizationSerializer()
    class Meta:
        model = Profile
        fields = ["userid", "birth_date", "gender", "education", "address", "group", "organization", "country"]

class StudentListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    premium = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'picture', 'last_login', 'profile', 'premium', "email", "phone"]

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
    profile = ProfileSerializer(many=True)
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


#* Stude update

class UpdateProfileSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    organization = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_organization=True), required=False)
    class Meta:
        model = Profile
        fields = ['address', 'gender', 'birth_date', 'country', 'education', 'group', 'organization']

class StudentUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    profile = UpdateProfileSerializer(required=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    organization = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_organization=True), required=False)

    def create(self, validated_data):
        user_id = self.context.get('id')
        with transaction.atomic():
            user = User.objects.get(id=user_id)
            user.full_name = validated_data.get('full_name', user.full_name)
            user.email = validated_data.get('email', user.email)
            user.phone = validated_data.get('phone', user.phone)
            user.save()

            profile_instance, created = Profile.objects.get_or_create(user=user)
            profile_data = validated_data.get('profile', {})

            group_instance = validated_data.get('group')
            organization_instance = validated_data.get('organization')

            group_id = group_instance.id if group_instance else (profile_instance.group.id if profile_instance.group else None)
            organization_id = organization_instance.id if organization_instance else (profile_instance.organization.id if profile_instance.organization else None)

            profile_data['group'] = group_id
            profile_data['organization'] = organization_id

            profile_serializer = UpdateProfileSerializer(profile_instance, data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()

            return user
