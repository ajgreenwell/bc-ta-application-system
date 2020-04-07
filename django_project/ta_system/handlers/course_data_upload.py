from uuid import uuid4
from django.db import IntegrityError as AlreadyExistsError
from ..models import Course, Semester, Instructor
from ta_system.data_formats.course_data_formats import (
    DATA_FORMATS,
    EXPECTED_LINE_FORMAT
)
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)


def handle_course_data_upload(file):
    handle_file_upload(
        file=file,
        destination=f'{FILE_UPLOAD_DESTINATION}{str(uuid4())}.csv',
        process_data_callback=process_course_data
    )


def process_course_data(fname):
    with open(fname, 'r') as courses:
        validate_csv_data(courses, EXPECTED_LINE_FORMAT)
        validate_course_data(courses)
        for course in courses:
            process_course(course)


def validate_course_data(courses):
    unique_course_ids = set()
    for course in courses:
        semester, course_number = course.split(',')[:2]
        course_id = f'({semester}: {course_number})'
        if course_id in unique_course_ids:
            raise ValueError(course_id)
        course_obj = Course.objects.filter(
            semester__semester=semester,
            course_number=course_number
        )
        if course_obj:
            raise AlreadyExistsError(course_id)
        unique_course_ids.add(course_id)
    courses.seek(0)


def process_course(course_data):
    course_data = dict(zip(DATA_FORMATS.keys(), course_data.split(',')))
    course = Course(
        semester=get_semester(course_data),
        course_number=course_data['course_number'],
        name=course_data['name'],
        instructor=get_instructor(course_data),
        days_of_week=course_data['days_of_week'],
        start_time=course_data['start_time'],
        end_time=course_data['end_time'],
        building=course_data['building'],
        room_number=course_data['room_number'],
        max_num_tas=course_data['max_num_tas']
    )
    course.save()


def get_semester(course_data):
    try:
        semester = Semester.objects.get(semester=course_data['semester'])
    except Semester.DoesNotExist:
        semester = Semester(semester=course_data['semester'])
        semester.save()
    return semester


def get_instructor(course_data):
    try:
        instructor = Instructor.objects.get(name=course_data['instructor'])
    except Instructor.DoesNotExist:
        instructor = Instructor(name=course_data['instructor'])
        instructor.save()
    return instructor
