from rest_framework import serializers

from accounts.models import User

from .models import Discussion


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "picture", "id"
        ]

class DiscussionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like = UserSerializer(many=True)
    # replies = DiscussionSerializer(many=True)
    class Meta:
        model = Discussion
        fields = [
            "total_like",
            "like",
            "user",
            "total_replies"
        ]