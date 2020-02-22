from ..models import Course, Instructor
from ..utils.file_uploads import get_timestamped_fname, handle_file_upload
from os import remove


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
    fname = get_timestamped_fname('Course_Data', 'csv')
    handle_file_upload(
        file=file,
        destination=f'ta_system/static/course_data/{fname}',
        process_data_callback=process_course_data
    )


def process_course_data(fname):
    with open(fname, 'r') as courses:
        validate_all_courses(courses)
        for course in courses:
            process_course(course.split(','))


def validate_all_courses(file):
    for line_number, line in enumerate(file):
        course_data = line.split(',')
        if not is_valid(course_data):
            file.close()
            remove(file.name)
            raise TypeError(f'Invalid course data –– expected {len(COURSE_DATA_VALUES)} comma separated ' +
                            f'values per line, but received {len(course_data)} on line {line_number + 1}.')
    file.seek(0)


def is_valid(course_data):
    return len(course_data) == len(COURSE_DATA_VALUES)


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
