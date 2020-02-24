from ..utils.file_uploads import handle_file_upload, FILE_UPLOAD_DESTINATION
from uuid import uuid4


def handle_applicant_data_upload(file):
    handle_file_upload(
        file=file,
        destination=f'{FILE_UPLOAD_DESTINATION}{str(uuid4())}.csv',
        process_data_callback=process_applicant_data
    )


def process_applicant_data(fname):
    with open(fname, 'r') as applicant_data:
        validate_applicant_data(applicant_data)
        for row in applicant_data:
            process_applicant_data(row.split(','))


def validate_applicant_data(file):
    pass


def process_applicant_data(applicant_data):
    pass