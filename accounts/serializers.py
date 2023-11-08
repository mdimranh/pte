from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .models import User, SocialAccount


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_student'] = True
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user

PROVIDERS = [
    ("facebook", "Facebook"),
    ("google", "Google"),
    ("apple", "Apple")
]

class SocialRegistrationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    image_url = serializers.URLField(allow_blank=True, max_length=1000)
    provider = serializers.ChoiceField(choices=PROVIDERS)

    def create(self, validated_data):
        user_data = {
            "full_name": validated_data['full_name'],
            "email": validated_data['email'],
            'is_student': True
        }
        if 'image_url' in validated_data and validated_data['image_url'] is not None:
            user_data['image_url'] = validated_data['image_url']
        user = User.objects.create(**user_data)
        saccount = SocialAccount.objects.create(
            user = user,
            uid = validated_data['uid'],
            provider = validated_data['provider']
        )
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', "full_name", "phone",)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('email', 'password')

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'full_name', 'picture']

class UserProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    full_name = serializers.CharField(max_length=255, required=False)