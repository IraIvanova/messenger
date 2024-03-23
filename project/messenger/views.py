from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from project.utils import ErrorConstants
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
import json
from .models import Chat, Message, UserStatus
from .forms import CreateChatForm, CreateMessageForm
from .utils import (
    get_chats_list_for_user,
    get_data_for_template,
    get_chat_and_message)
from .mixins import (
    MyLoginRequiredMixin,
    SuperuserOrPermissionRequiredMixin,
    AjaxRequiredMixin,
    CreateSuccessMessageMixin)


class ChatListPage(MyLoginRequiredMixin, View):
    index_template_name = 'chat_list.html'
    show_template_name = 'chat.html'

    def get(self, request, id=None):
        chats = get_chats_list_for_user(request.user)

        data = {
            'chats': chats
        }

        if id:
            get_data_for_template(request.user, id, data)

            return render(request, self.show_template_name, data)

        return render(request, self.index_template_name, data)


class ChatCreateForm(CreateSuccessMessageMixin, SuperuserOrPermissionRequiredMixin, View):
    permission_required = 'messenger.add_chat'
    template_name = 'create_chat.html'
    login_url = '/users/login/'
    success_message = 'Chat successfully created!'

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
            self.processed_successfully(request)
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
            recipient = get_user_model().objects.filter(email=form.cleaned_data.get('recipient')).first()

            message = Message(
                message=msg,
                author=user,
                chat=chat,
                recipient=recipient
            )
            message.save()

            return redirect('show_chat', id=chat.id)


class DeleteMessageAction(AjaxRequiredMixin, View):
    def post(self, request):
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


def check_statuses(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    if not chat:
        return JsonResponse({'error': 'Chat not found'}, status=404)

    members = chat.members.all()
    user_statuses = {}

    for member in members:
        try:
            user_statuses[member.id] = member.user_status.online
        except UserStatus.DoesNotExist:
            user_statuses[member.id] = False

    return JsonResponse(user_statuses)
