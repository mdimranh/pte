from django.db import IntegrityError, transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from management.models import Profile

from .models import *


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
            user.save()
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
        user.save()
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
        fields = ['id', 'full_name', 'phone', 'email', 'picture', 'profile']

    def get_profile(self, obj):
        profile = Profile.objects.filter(user__id=obj.id).first()
        if profile is not None:
            return OrgProfileSerializer(instance=profile).data
        return {}

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['org_name', 'address', 'country']

class OrganizationUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    profile = UpdateProfileSerializer(required=False)

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

            profile_serializer = UpdateProfileSerializer(profile_instance, data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
            return user


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class DynamicSerializer:
    def __init__(self, model):
        self.model = model

    def generate(self, fields, _for, main):
        fields.append("discussions_count")
        fields.append("last_discussion_date")

        return type("DynamicSerializer", (serializers.ModelSerializer,), {
            "discussions_count": serializers.SerializerMethodField(),
            "last_discussion_date": serializers.SerializerMethodField(),
            "Meta": type('Meta', (), {'model': _for, 'fields': fields}),
            "get_discussions_count": self.get_discussions_count,
            "get_last_discussion_date": self.get_last_discussion_date,
        })

    def get_discussions_count(self, obj):
        return obj.discussion.count()

    def get_last_discussion_date(self, obj):
        discussion = obj.discussion.last()
        if discussion is not None:
            return discussion.created_at


class PromoBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoBanner
        fields = '__all__'