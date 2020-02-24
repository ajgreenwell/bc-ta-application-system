from django.utils import timezone
from os import remove as delete_uploaded_file

FILE_UPLOAD_DESTINATION = 'ta_system/static/file_uploads/'


def handle_file_upload(file, destination, process_data_callback):
    extension = get_extension_from_fname(destination)
    if not file.name.endswith(f'.{extension}'):
        raise TypeError(f'Invalid file type –– must upload a {extension} file.')
    save_uploaded_file(file, destination)
    process_data_callback(destination)
    delete_uploaded_file(destination)


def get_extension_from_fname(fname):
    return fname[fname.rfind('.') + 1:]


def save_uploaded_file(file, destination):
    with open(destination, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
