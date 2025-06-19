# messaging_app/chats/urls.py

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
1
