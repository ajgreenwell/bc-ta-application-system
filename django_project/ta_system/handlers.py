from datetime import datetime
from .models import CourseNumber, Course, Instructor


def handle_course_data_upload(file):
    path = 'ta_system/static/course_data/'
    filename = get_course_data_filename()

    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    with open(path + filename, 'r') as f:
        for line in f:
            process_course_data(line)


def get_course_data_filename():
    date = datetime.now()
    return f'Course_Data_{date.strftime("%b")}_{date.year}'


def process_course_data(course):
    pass

