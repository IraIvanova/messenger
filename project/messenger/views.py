from django.shortcuts import render, redirect
from django.views import View
from .models import Chat, Message
from .forms import CreateChatForm, CreateMessageForm
from project.utils import ErrorConstants
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .utils import (
    get_chats_list_for_user,
    get_chat_for_user,
    get_chat_and_data,
    get_chat_and_message)
from django.contrib.auth.decorators import login_required
import json


class ChatListPage(LoginRequiredMixin, View):
    index_template_name = 'chat_list.html'
    show_template_name = 'chat.html'
    login_url = '/users/login/'

    def get(self, request, id=None):
        chats = get_chats_list_for_user(request.user)

        data = {
            'chats': chats
        }

        if id:
            user = request.user
            chat = get_chat_for_user(user, id)

            if not chat:
                return render(request, ErrorConstants.error_404_template, {})

            chat, data = get_chat_and_data(request.user, id)

            return render(request, self.show_template_name, data)

        return render(request, self.index_template_name, data)


class ChatCreateForm(PermissionRequiredMixin, View):
    permission_required = 'messenger.add_chat'
    template_name = 'create_chat.html'
    login_url = '/users/login/'

    def get(self, request):
        form = CreateChatForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateChatForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            chat, create = Chat.objects.get_or_create(title=title)
            chat.members.add(*form.cleaned_data.get('members'))
            chat.save()
        return redirect('chats')


class MessagesAction(View):
    show_template_name = 'chat.html'

    def post(self, request):
        form = CreateMessageForm(request.POST)
        if form.is_valid():
            user = request.user
            chat = Chat.objects.get(pk=form.cleaned_data.get('chat'))

            if not chat or not user:
                return render(request, ErrorConstants.error_404_template, {})

            msg = form.cleaned_data.get('message')

            message = Message(
                message=msg,
                author=user,
                chat=chat
            )
            message.save()

            return redirect('show_chat', id=chat.id)


@login_required
def delete_message(request):
    data = json.loads(request.body)
    form = CreateMessageForm(data)

    if form.is_valid():
        user = request.user
        chat, message = get_chat_and_message(form.cleaned_data.get('chat'), form.cleaned_data.get('message_id'))

        if not chat or not user:
            return render(request, ErrorConstants.error_404_template, {})

        if message.author != user:
            return HttpResponse('Forbidden', status=403)

        message.delete()

        return HttpResponse(json.dumps({'message': 'The message changed successfully'}), status=200)


@login_required
def edit_message(request):
    data = json.loads(request.body)
    form = CreateMessageForm(data)

    if form.is_valid():
        user = request.user
        chat, message = get_chat_and_message(form.cleaned_data.get('chat'), form.cleaned_data.get('message_id'))

        if not chat or not user:
            return render(request, ErrorConstants.error_404_template, {})

        if message.author != user:
            return HttpResponse('Forbidden', status=403)

        message.message = form.cleaned_data.get('message')
        message.save()

        return HttpResponse(json.dumps({'message': 'The message changed successfully'}), status=200)
