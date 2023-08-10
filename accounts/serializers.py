from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
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