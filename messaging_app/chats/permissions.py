from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    Assumes the object has a `.conversation` with `.sender` and `.receiver`.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if user is part of the conversation
        return hasattr(obj, "conversation") and (
            user == obj.conversation.sender or user == obj.conversation.receiver
        )
