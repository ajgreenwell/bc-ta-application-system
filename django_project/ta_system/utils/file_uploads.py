from django.utils import timezone


def handle_file_upload(file, destination, process_data_callback):
    extension = get_extension_from_fname(destination)
    if not file.name.endswith(f'.{extension}'):
        raise TypeError(f'Invalid file type –– must upload a {extension} file.')

    save_uploaded_file(file, destination)
    process_data_callback(destination)


def get_extension_from_fname(fname):
    return fname[fname.rfind('.') + 1:]


def save_uploaded_file(file, destination):
    with open(destination, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def get_timestamped_fname(fname, extension):
    date = timezone.localtime(timezone.now())
    return f'{fname}__{timestamp(date)}.{extension}'


def timestamp(datetime_obj):
    d = datetime_obj
    return f'{d.strftime("%b")}_{d.day}_{d.year}__{d.hour}:{d.minute}:{d.second}'