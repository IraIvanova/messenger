from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserChatsAPIView,
    UserChatMessagesAPIView,
    MessageDetailsAPIView,
    ChatCreateAPIView,
    MessageCreateAPIView
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/chats/', UserChatsAPIView.as_view(), name='user_chats'),
    path('api/user/chats/add', ChatCreateAPIView.as_view()),
    path('api/user/chat/<int:chat_id>/messages/', UserChatMessagesAPIView.as_view(), name='user_chat_messages'),
    path('api/message/<int:pk>/', MessageDetailsAPIView.as_view(), name='message_details'),
    path('api/message/add', MessageCreateAPIView.as_view()),
]
