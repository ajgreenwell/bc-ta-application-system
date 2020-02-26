from uuid import uuid4
from ta_system.models import Course, Profile
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)


APPLICANT_DATA_VALUES = [
    'count',
    'term',
    'last_name',
    'first_name',
    'username',
    'eagle_id',
    'course_num',
    'course_title'
]


def handle_applicant_data_upload(file):
    handle_file_upload(
        file=file,
        destination=f'{FILE_UPLOAD_DESTINATION}{str(uuid4())}.csv',
        process_data_callback=process_applicant_data
    )


def process_applicant_data(fname):
    with open(fname, 'r') as applicant_data:
        validate_csv_data(applicant_data, len(APPLICANT_DATA_VALUES))
        for row in applicant_data:
            process_applicant(row.split(','))


def process_applicant(applicant_data):
    applicant_data = dict(zip(APPLICANT_DATA_VALUES, applicant_data))
    course = Course.objects.get(cours_num=applicant_data['course_num'])
    applicant = Profile.objects.get(eagle_id=applicant_data['eagle_id'])
    applicant.courses_taken.add(course)
