from django.db import IntegrityError, transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from management.models import Profile

from .models import StudyMaterial


class SuperAdminCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    userid = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    phone = PhoneNumberField()


    def create(self, validated_data):
        with transaction.atomic():
            user_data = {
                'is_staff': True,
                "full_name": validated_data.get('full_name'),
                "email": validated_data['email'],
                "phone": validated_data['phone']
            }
            user = User.objects.create_user(**user_data)
            user.set_password(validated_data['password'])
            profile, create = Profile.objects.get_or_create(
                user=user
            )
            profile.userid = validated_data['userid']
            profile.save()
            return user

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'organization', 'group', 'user', 'org_name']

class AdminUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone', 'email', 'picture', 'profile']

    def get_profile(self, obj):
        profile = Profile.objects.filter(user__id=obj.id).first()
        if profile is not None:
            return AdminProfileSerializer(instance=profile).data
        return {}

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = '__all__'

class CreateOrganizationSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    full_name = serializers.CharField()
    country = serializers.CharField(required=True)
    org_name = serializers.CharField(required=True)
    phone = PhoneNumberField()


    def create(self, validated_data):
        user_data = {
            'is_organization': True,
            "full_name": validated_data.get('full_name'),
            "email": validated_data['email']
        }
        if "phone" in validated_data:
            user_data['phone'] = validated_data['phone']
        user = User.objects.create_user(**user_data)
        user.set_password(validated_data['password'])
        profile, create = Profile.objects.get_or_create(
            user=user
        )
        profile.userid = validated_data['userid']
        profile.org_name = validated_data['org_name']
        profile.country = validated_data['country']
        profile.save()
        return user


class OrgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'organization', 'group', 'user']

class OrganizationSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'email', 'picture', 'profile']

    def get_profile(self, obj):
        profile = Profile.objects.filter(user__id=obj.id).first()
        if profile is not None:
            return OrgProfileSerializer(instance=profile).data
        return {}