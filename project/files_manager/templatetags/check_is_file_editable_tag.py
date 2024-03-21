from django import template
from files_manager.utils import check_is_file_editable
import os

register = template.Library()


@register.simple_tag()
def check_is_file_editable_tag(file):
    return check_is_file_editable(file)
