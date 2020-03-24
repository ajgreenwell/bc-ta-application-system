from django.utils import timezone
from os import remove as delete_uploaded_file
import re


FILE_UPLOAD_DESTINATION = 'ta_system/static/file_uploads/'
UPLOAD_DATA_FORMATS_URL = 'https://docs.google.com/document/d/1d5URLk7UtipN-KJIybzBFmEEip9_YA8Ove4UV3uLBwQ/edit?usp=sharing'
UPLOAD_DATA_FORMATS_LINK= f'<a href={UPLOAD_DATA_FORMATS_URL} target="_blank">here</a>'


def handle_file_upload(file, destination, process_data_callback):
    extension = get_extension_from_fname(destination)
    if not file.name.endswith(extension):
        raise TypeError(f'Invalid file type –– must upload a {extension} file')
    save_uploaded_file(file, destination)
    try:
        process_data_callback(destination)
    except:
        delete_uploaded_file(destination)
        raise
    else:
        delete_uploaded_file(destination)


def get_extension_from_fname(fname):
    return fname[fname.rfind('.'):]


def save_uploaded_file(file, destination):
    with open(destination, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def validate_csv_data(file, expected_line_format):
    expected_line_format = re.compile(expected_line_format)
    for line_number, line in enumerate(file):
        if not is_valid_csv_line(line, expected_line_format):
            raise TypeError(
                f'Invalidly formatted data on line {line_number + 1}. ' + 
                f'Click {UPLOAD_DATA_FORMATS_LINK} to see documentation ' +
                'on how your data should be formatted'
            )
    file.seek(0)


def is_valid_csv_line(line, expected_line_format):
    return expected_line_format.fullmatch(line.rstrip('\n'))
