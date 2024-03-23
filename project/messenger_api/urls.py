from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserChatsAPIView,
    UserChatMessagesAPIView,
    ChatCreateAPIView,
    MessageCrudAPIView,
    login_view
)


urlpatterns = [
    path('login/', login_view),
    path('user/chats/', UserChatsAPIView.as_view()),
    path('chats/add/', ChatCreateAPIView.as_view()),
    path('chats/<int:chat>/<int:user>/messages/', UserChatMessagesAPIView.as_view()),
    path('message/add', MessageCrudAPIView.as_view()),
    path('message/<int:pk>/edit', MessageCrudAPIView.as_view()),
    path('message/<int:pk>/delete', MessageCrudAPIView.as_view()),
]
