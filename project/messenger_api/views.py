from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from messenger.models import Chat, Message
from custom_user.models import CustomUser
from .serializers import ChatSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
import json


class UserChatsAPIView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    user = False

    def get_queryset(self):
        return Chat.objects.filter(members=self.user)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.query_params.get('user'))

        if not user:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.user = user

        return super().get(request, *args, **kwargs)


class UserChatMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        params = self.kwargs
        return Message.objects.filter(chat_id=params['chat'], author_id=params['user'])

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.filter(pk=self.kwargs['user'])
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        chat = get_object_or_404(Chat, id=self.kwargs['chat'])

        if not chat.members.filter(id=user.id).exists():
            return Response({"message": "User is not a member of the chat."}, status=status.HTTP_404_NOT_FOUND)

        return super().get(request, *args, **kwargs)


class MessageDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(service_msg=False, author=self.request.user)


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        post_data = request.data

        if not user.has_perm('messenger.add_chat'):
            return Response({'error': 'You do not have permission to create a chat.'}, status=status.HTTP_403_FORBIDDEN)

        if Chat.objects.filter(title=post_data.get('title')):
            return Response({'error': 'Chat with same title already exists.'}, status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)


class MessageCrudAPIView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(service_msg=False, author=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_data = request.data

        if not Chat.objects.filter(members=user, pk=post_data.get('chat')).exists():
            return Response({'error': 'Chat does not exist or you\'re not the member of this chat'},
                            status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)

    def validate_chat_and_message(self, chat_id, message_id):
        user = self.request.user

        # Check if the user is a member of the specified chat
        if not Chat.objects.filter(members=user, pk=chat_id).exists():
            return False, Response({'error': 'Chat does not exist or you are not a member of this chat'},
                                   status=status.HTTP_404_NOT_FOUND)

        # Check if the message exists and the user is its author
        if not Message.objects.filter(pk=message_id, author=user, service_msg=False).exists():
            return False, Response({'error': 'Message does not exist or you are not the author of this message'},
                                   status=status.HTTP_404_NOT_FOUND)

        return True, None

    def update(self, request, *args, **kwargs):
        chat_id = request.data.get('chat')
        message_id = kwargs.get('pk')
        allowed, response = self.validate_chat_and_message(chat_id, message_id)
        if not allowed:
            return response
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        chat_id = request.data.get('chat')
        message_id = kwargs.get('pk')
        allowed, response = self.validate_chat_and_message(chat_id, message_id)
        if not allowed:
            return response
        return super().delete(request, *args, **kwargs)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        login(request, user)

        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
