from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import StudyMaterial
from management.models import Profile
from accounts.models import User


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

class ProfileSerializer(serializers.ModelSerializer):
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
            return ProfileSerializer(instance=profile).data
        return {}