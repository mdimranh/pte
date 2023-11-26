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
            "full_name", "email", "picture", "id"
        ]

class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like = UserSerializer(many=True)
    self_like = serializers.SerializerMethodField()
    
    class Meta:
        model = Discussion
        fields = [
            "id",
            'body',
            "images",
            'self_like',
            "like",
            "user",
            "created_at"
        ]

    def get_self_like(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user in obj.like.all()
        return False

class DiscussionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like = UserSerializer(many=True)
    replies = serializers.SerializerMethodField()
    self_like = serializers.SerializerMethodField()
    class Meta:
        model = Discussion
        fields = [
            # "total_like",
            "id",
            "self_like",
            'body',
            "images",
            "like",
            "user",
            "replies",
            "created_at"
        ]

    def get_replies(self, obj):
        # Implement your logic to serialize replies here
        replies = Discussion.objects.filter(parent=obj)
        serializer = ReplySerializer(replies, many=True, context=self.context)
        return serializer.data

    def get_self_like(self, obj):
        # Add your logic to calculate self_like here
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like.all()
        return False

class DynamicSerializer:
    def __init__(self, model):
        self.model = model

    def generate(self, fields, _for, main):
        fields.append(main)
        return type("DynamicSerializer", (serializers.ModelSerializer,),{
            f"{main}": serializers.PrimaryKeyRelatedField(queryset=_for.objects.all()),
            "Meta": type('Meta', (), {'model': Discussion, 'fields': fields})
        })
