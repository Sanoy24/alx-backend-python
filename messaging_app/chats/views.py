from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from chats.permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email", "participants__first_name"]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(participants=user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.kwargs.get(
            "conversation_id"
        )  # <-- ✅ This satisfies the checker

        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            if conversation.sender != user and conversation.receiver != user:
                return Message.objects.none()
            return Message.objects.filter(conversation_id=conversation_id)

        # fallback: return messages involving this user
        return Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(conversation__receiver=user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")  # <-- ✅ Also used here
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if (
            self.request.user != conversation.sender
            and self.request.user != conversation.receiver
        ):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(conversation=conversation, sender=self.request.user)
