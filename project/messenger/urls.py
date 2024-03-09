from django.urls import path
from .views import ChatListPage, ChatCreateForm, MessagesAction, edit_message, delete_message

urlpatterns = [
    path('chat', ChatListPage.as_view(), name='chats'),
    path('create-chat', ChatCreateForm.as_view(), name='create_chat'),
    path('chat/<int:id>', ChatListPage.as_view(), name='show_chat'),
    path('send_message', MessagesAction.as_view(), name='send_message'),
    path('edit_message', edit_message, name='edit_message'),
    path('delete_message', delete_message, name='delete_message'),
]
