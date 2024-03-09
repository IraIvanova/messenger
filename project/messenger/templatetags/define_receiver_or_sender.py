from django import template

register = template.Library()


@register.simple_tag()
def define_receiver_or_sender(author, auth_user):
    if auth_user.id == author.id:
        return 'sender'
    else:
        return 'receiver'
