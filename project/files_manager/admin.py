from django.contrib import admin
from .models import File

class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file')


admin.site.register(File, FilesAdmin)