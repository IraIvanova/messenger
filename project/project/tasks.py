from .celery import shared_task
from messenger.models import Message
import logging

logger = logging.getLogger('last_messages_logger')


@shared_task
def log_last_10_messages():
    logger.info('*-*-messages-*-*')
    last_10_messages = Message.objects.order_by('-timestamp')[:10]
    for message in last_10_messages:
        logger.info(message.text)
