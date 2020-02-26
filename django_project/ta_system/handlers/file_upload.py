from django.utils import timezone
from os import remove as delete_uploaded_file


FILE_UPLOAD_DESTINATION = 'ta_system/static/file_uploads/'


def handle_file_upload(file, destination, process_data_callback):
    extension = get_extension_from_fname(destination)
    if not file.name.endswith(f'.{extension}'):
        raise TypeError(f'Invalid file type –– must upload a {extension} file.')

    save_uploaded_file(file, destination)
    try:
        process_data_callback(destination)
    except:
        delete_uploaded_file(destination)
        raise
    else:
        delete_uploaded_file(destination)


def get_extension_from_fname(fname):
    return fname[fname.rfind('.') + 1:]


def save_uploaded_file(file, destination):
    with open(destination, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def validate_csv_data(file, num_expected_values):
    for line_number, line in enumerate(file):
        data = line.split(',')
        if not is_valid_csv_line(data, num_expected_values):
            raise TypeError(f'Invalid applicant data –– expected {num_expected_values} comma separated ' +
                            f'values per line, but received {len(data)} on line {line_number + 1}.')
    file.seek(0)


def is_valid_csv_line(data, num_expected_values):
    return len(data) == num_expected_values
