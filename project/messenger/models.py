from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Chat(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(get_user_model())


class Message(models.Model):
    class Meta:
        permissions = (
            ("can_edit_own_message", "User can edit own message"),
        )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages',
                                  null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    service_msg = models.BooleanField(default=False)

    def reply_to_sender(self):
        sender_message = "You have successfully sent a message to the superuser!"
        Message.objects.create(author=self.author, recipient=self.author, message=sender_message, chat_id=self.chat_id, service_msg=True)


class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_status')
    online = models.BooleanField(default=False)
