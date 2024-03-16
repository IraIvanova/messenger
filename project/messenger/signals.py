from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
import logging

logger = logging.getLogger('message_logger')

@receiver(post_save, sender=Message)
def log_sent_message(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Message `{instance.message}` sent by {instance.author.username} in chat {instance.chat.title} at {instance.created_at}.")
        if instance.recipient and instance.recipient.is_superuser:
            instance.reply_to_sender()