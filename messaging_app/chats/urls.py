# messaging_app/chats/urls.py

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Base router
router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# Nested router for messages under conversations
conversation_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
conversation_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversation_router.urls)),
]
1
