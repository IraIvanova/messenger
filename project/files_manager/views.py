from django.shortcuts import render, redirect, get_object_or_404
import os
from .models import File
from .forms import FileForm
from .utils import check_is_file_editable, generate_unique_filename


def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            uploaded_file = request.FILES['file']
            file_instance.file.name = generate_unique_filename(uploaded_file)
            file_instance.save()

    return redirect('files_list')


def file_list(request):
    files = File.objects.all()
    form = FileForm()
    return render(request, 'files_list.html', {'files': files, 'form': form})


def edit_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if not check_is_file_editable(file):
        return redirect('files_list')

    if request.method == 'POST':
        content = request.POST.get('content', '')
        with open(file.file.path, 'w') as f:
            f.write(content)
        return redirect('files_list')
    else:
        content = file.file.read().decode('utf-8')
    return render(request, 'edit_file.html', {'file': file, 'content': content})
