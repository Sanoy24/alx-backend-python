from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]
        read_only_fields = ["user_id"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class NestedUserSerializer(serializers.ModelSerializer):
    """Used when displaying participants/messages"""

    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email"]


class MessageSerializer(serializers.ModelSerializer):
    sender = NestedUserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "sender_id",
            "conversation",
            "message_body",
            "sent_at",
            "is_read",
        ]
        read_only_fields = ["message_id", "sent_at"]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def create(self, validated_data):
        sender_id = validated_data.pop("sender_id")
        validated_data["sender"] = User.objects.get(user_id=sender_id)
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    participants = NestedUserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "participant_ids",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        if users.count() != len(participant_ids):
            raise serializers.ValidationError("One or more users not found.")
        conversation.participants.set(users)
        return conversation
