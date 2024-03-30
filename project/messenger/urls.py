from django.urls import path
from .views import ChatListPage, ChatCreateForm, MessagesAction, edit_message, DeleteMessageAction, check_statuses

urlpatterns = [
    path('chat', ChatListPage.as_view(), name='chats'),
    path('create-chat', ChatCreateForm.as_view(), name='create_chat'),
    path('chat/<int:id>', ChatListPage.as_view(), name='show_chat'),
    path('send_message', MessagesAction.as_view(), name='send_message'),
    path('edit_message', edit_message, name='edit_message'),
    path('delete_message', DeleteMessageAction.as_view(), name='delete_message'),
    path('get_user_statuses/<int:chat_id>/', check_statuses, name='check_statuses'),
]
