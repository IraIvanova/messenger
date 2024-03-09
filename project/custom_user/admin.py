from django.contrib import admin
from custom_user.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(CustomUser, CustomUserAdmin)
