from os import remove
from uuid import uuid4
from django.db import IntegrityError as AlreadyExistsError
from ..models import Course, Instructor
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)


EXPECTED_LINE_FORMAT = '[A-Z]+\d+,\S+( \S+)*,\S+( \S+)*,[MTWRFAS](/[MTWRFAS])*,' + \
                       '\d{2}:\d{2}(:\d{2})*/\d{2}:\d{2}(:\d{2})*,\S+( \S+)* \w+,\d+'
COURSE_DATA_VALUES = [
    'course_number',
    'name',
    'instructor',
    'days_of_week',
    'start_end_times',
    'building_and_room',
    'max_num_tas'
]


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
        delete_all_existing_courses()
        for course in courses:
            process_course(course)


def validate_course_data(courses):
    unique_course_numbers = set()
    for course in courses:
        course_number = course.split(',')[0]
        if course_number in unique_course_numbers:
            raise ValueError(course_number)
        unique_course_numbers.add(course_number)
    courses.seek(0)


def delete_all_existing_courses():
    delete_courses({course.course_number for course in Course.objects.all()})


def delete_courses(course_numbers):
    for number in course_numbers:
        Course.objects.filter(course_number=number).delete()


def process_course(course_data):
    course_data = dict(zip(COURSE_DATA_VALUES, course_data.split(',')))
    instructor = get_instructor(course_data)
    (start_time, end_time) = course_data['start_end_times'].split('/')
    (building, room_number) = course_data['building_and_room'].split(' ')
    course = Course(
        course_number=course_data['course_number'],
        name=course_data['name'],
        instructor=instructor,
        days_of_week=course_data['days_of_week'],
        start_time=start_time,
        end_time=end_time,
        building=building,
        room_number=room_number,
        max_num_tas=course_data['max_num_tas']
    )
    course.save()


def get_instructor(course_data):
    try:
        instructor = Instructor.objects.get(name=course_data['instructor'])
    except Instructor.DoesNotExist:
        instructor = Instructor(name=course_data['instructor'])
        instructor.save()
    return instructor
