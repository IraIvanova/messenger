from django import template

register = template.Library()


@register.simple_tag()
def define_receiver_or_sender(msg, auth_user):
    if auth_user.id == msg.author.id and not msg.service_msg:
        return 'sender'
    elif msg.service_msg:
        return 'service'
    else:
        return 'receiver'
