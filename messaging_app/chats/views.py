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
        return Message.objects.filter(
            conversation__sender=user
        ) | Message.objects.filter(conversation__receiver=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not IsParticipantOfConversation().has_object_permission(
            request, self, instance
        ):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)
