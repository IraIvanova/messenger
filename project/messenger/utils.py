from .models import Chat, Message
from django.db.models import Q
from .forms import CreateMessageForm

def get_chats_list_for_user(user):
    if user.is_superuser:
        return Chat.objects.all()
    else:
        return Chat.objects.filter(members=user)


def get_chat_for_user(user, id):
    if user.is_superuser:
        return Chat.objects.get(pk=id)
    else:
        return Chat.objects.get(Q(members=user) & Q(pk=id))


def get_chat_messages(chat):
    return Message.objects.filter(chat=chat)


def get_data_for_template(user, chat_id, data):
    chat = get_chat_for_user(user, chat_id)

    if chat:
        messages = chat.messages.all()
        form = CreateMessageForm({'author': user.id, 'chat': chat_id})
        data.update({'chat': chat, 'form': form, 'messages': messages})


def get_chat_and_message(chat_id, message_id):
    chat = Chat.objects.filter(pk=chat_id).first()
    message = Message.objects.filter(pk=message_id).first()
    return chat, message