from django import template
from datetime import datetime, timezone

register = template.Library()


@register.simple_tag()
def is_edit_date_not_expired(created_date):
    current_datetime = datetime.now(timezone.utc)
    return (current_datetime - created_date).days < 1


