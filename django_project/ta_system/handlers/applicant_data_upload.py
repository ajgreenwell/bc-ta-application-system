from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist
from ta_system.models import Course, Profile
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)

EXPECTED_LINE_FORMAT = '\d{4}[FS],\S+,\S+,\S+,\d{8},[A-Z]+\d+,\S+( \S+)*'
APPLICANT_DATA_VALUES = [
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
        validate_csv_data(applicant_data, EXPECTED_LINE_FORMAT)
        for row in applicant_data:
            process_applicant(row.split(','))


def process_applicant(applicant_data):
    applicant_data = dict(zip(APPLICANT_DATA_VALUES, applicant_data))
    try:
        course = Course.objects.get(course_num=applicant_data['course_num'])
        applicant = Profile.objects.get(eagle_id=applicant_data['eagle_id'])
    except Course.DoesNotExist:
        raise ObjectDoesNotExist('The following course does not exist in our database: ' +
                                f'{applicant_data["course_num"]}: {applicant_data["course_title"]}')
    except Profile.DoesNotExist:
        raise ObjectDoesNotExist('The following applicant does not exist in our database: ' +
                                f'{applicant_data["first_name"]} {applicant_data["last_name"]}')
    else:
        applicant.courses_taken.add(course)
