from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from messenger.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class UserChatsAPIView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class UserChatMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id, author=self.request.user)


class MessageDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        post_data = request.POST
        chat = Chat.objects.get(pk=post_data.get('chat'))

        if not request.user.has_perm('messenger.add_chat'):
            return Response({'error': 'You do not have permission to create a chat.'}, status=status.HTTP_403_FORBIDDEN)

        if not chat:
            return Response({'error': 'Chat does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)