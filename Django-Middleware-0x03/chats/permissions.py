from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    Explicitly checks for PUT, PATCH, DELETE methods to satisfy requirement.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Explicitly check allowed methods
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return hasattr(obj, "conversation") and (
                user == obj.conversation.sender or user == obj.conversation.receiver
            )

        return False
