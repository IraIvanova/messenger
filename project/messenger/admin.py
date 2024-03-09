from django.contrib import admin
from .models import Chat

class ChatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Chat, ChatsAdmin)