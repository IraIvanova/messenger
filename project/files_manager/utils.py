import uuid
import os


def check_is_file_editable(file):
    try:
        file_extension = str(file.file).split('.')[1]
    except:
        return False

    return file_extension in ['txt', 'csv', 'log', 'py', 'php', 'html', 'css']


def generate_unique_filename(uploaded_file):
    original_filename, file_extension = os.path.splitext(uploaded_file.name)
    unique_filename = str(uuid.uuid4())[:16]  # Generate a unique filename using UUID
    new_filename = f"{unique_filename}{file_extension}"
    return new_filename
