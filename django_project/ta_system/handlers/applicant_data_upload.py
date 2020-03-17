from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist
from ta_system.models import Course, Profile
from ta_system.data_formats.applicant_data_formats import (
    DATA_FORMATS,
    EXPECTED_LINE_FORMAT
)
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)


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
    applicant_data = dict(zip(DATA_FORMATS.keys(), applicant_data))
    try:
        course = Course.objects.get(
            semester__semester=applicant_data['semester'],
            course_number=applicant_data['course_number']
        )
        applicant = Profile.objects.get(eagle_id=applicant_data['eagle_id'])
    except Course.DoesNotExist:
        raise ObjectDoesNotExist(
            'The following course does not exist in our database: ' +
            f'{applicant_data["semester"]}: {applicant_data["course_number"]}'
        )
    except Profile.DoesNotExist:
        raise ObjectDoesNotExist(
            'The following applicant does not exist in our database: ' +
            f'{applicant_data["eagle_id"]}: {applicant_data["first_name"]} {applicant_data["last_name"]}'
        )
    else:
        applicant.courses_taken.add(course)
