from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Message, UserStatus
import logging

logger = logging.getLogger('message_logger')


@receiver(post_save, sender=Message)
def log_sent_message(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"Message `{instance.message}` sent by {instance.author.username} in chat {instance.chat.title} at {instance.created_at}.")
        if instance.recipient and instance.recipient.is_superuser:
            instance.reply_to_sender()


@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):
    # Update user status to 'online' when the user logs in
    user_status, created = UserStatus.objects.get_or_create(user=user)
    user_status.online = True
    user_status.save()


@receiver(user_logged_out)
def user_logged_out_handler(sender, user, request, **kwargs):
    # Update user status to 'offline' when the user logs out
    user_status, created = UserStatus.objects.get_or_create(user=user)
    user_status.online = False
    user_status.save()
