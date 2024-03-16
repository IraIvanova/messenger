from django.urls import path
from .views import upload_file, file_list, edit_file

urlpatterns = [
    path('', file_list, name='files_list'),
    path('upload', upload_file, name='upload_files'),
    path('edit/<file_id>', edit_file, name='edit_file'),
    path('delete', edit_file, name='delete_file'),
]
