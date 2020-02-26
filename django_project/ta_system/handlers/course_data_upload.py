from os import remove
from uuid import uuid4
from ..models import Course, Instructor
from .file_upload import (
    handle_file_upload,
    validate_csv_data,
    FILE_UPLOAD_DESTINATION
)


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
        validate_csv_data(courses, len(COURSE_DATA_VALUES))
        for course in courses:
            process_course(course.split(','))


def process_course(course_data):
    course_data = dict(zip(COURSE_DATA_VALUES, course_data))
    instructor = get_instructor(course_data)
    (start_time, end_time) = course_data['start_end_times'].split('/')
    (building, room_number) = course_data['building_and_room'].split(' ')
    course = Course(
        course_num=course_data['course_number'],
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
    except:
        instructor = Instructor(name=course_data['instructor'])
        instructor.save()
    return instructor
