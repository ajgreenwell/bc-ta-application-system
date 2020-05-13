from ..models import Semester
from ..utils import get_verbose_semester
from .file_download import handle_file_download
from csv import writer
from django.http import HttpResponse
from io import StringIO
from ta_system.utils import get_year_and_semester_code


def handle_assignment_data_download(semester):
    def write_data(csv_writer):
        return write_ta_assignment_data(csv_writer, semester)

    headers = [
        'Semester', 'Course Number', 'Course Title', 'Professor',
        'TA Eagle ID', 'TA First Name', 'TA Last Name', 'TA Email'
    ]
    filename = f'{semester}_TA_Assignments.csv'
    return handle_file_download(headers, write_data, filename)


def write_ta_assignment_data(csv_writer, semester):
    semester_has_assigned_tas = False
    year, semester_code = get_year_and_semester_code(semester)
    courses = Semester.objects.get(
        year=year,
        semester_code=semester_code
    ).course_set.all()
    for course in courses:
        tas = course.teaching_assistants.all()
        if not semester_has_assigned_tas and tas:
            semester_has_assigned_tas = True
        for ta in tas:
            row = [
                course.semester, course.course_number,
                course.name, course.instructor.name,
                ta.eagle_id, ta.user.first_name,
                ta.user.last_name, ta.user.email
            ]
            csv_writer.writerow(row)
    if not semester_has_assigned_tas:
        raise ValueError(
            f'The semester ({get_verbose_semester(semester)}) has no ' +
            'courses to which any teaching assistants have been assigned'
        )
    return csv_writer
