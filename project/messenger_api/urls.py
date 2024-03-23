from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserChatsAPIView,
    UserChatMessagesAPIView,
    ChatCreateAPIView,
    MessageCrudAPIView
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user/chats/', UserChatsAPIView.as_view()),
    path('chats/add/', ChatCreateAPIView.as_view()),
    path('chats/<int:chat>/<int:user>/messages/', UserChatMessagesAPIView.as_view()),
    path('message/add', MessageCrudAPIView.as_view()),
    path('message/<int:pk>/edit', MessageCrudAPIView.as_view()),
    path('message/<int:pk>/delete', MessageCrudAPIView.as_view()),
]
