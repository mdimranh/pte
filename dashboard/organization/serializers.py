from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts.models import User
from management.models import Plan, Profile


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
    premium = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id', 'userid', 'group', 'premium']

    def get_premium(self, obj):
        return Profile.objects.get(pk=obj.pk).plan is not None

class StudentListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'full_name', 'picture', 'last_login','profile', ]

class ProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user', 'organization']

class StudentDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileDetailsSerializer(many=True)
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone", "picture", "profile"]