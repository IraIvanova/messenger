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
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

