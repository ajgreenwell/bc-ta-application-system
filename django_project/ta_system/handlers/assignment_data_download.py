from ..models import Semester
from ..utils import get_verbose_semester
from csv import writer
from django.http import HttpResponse
from io import StringIO
from ta_system.utils import get_year_and_semester_code


def handle_assignment_data_download(semester):
    csv_buffer = StringIO()
    csv_writer = writer(csv_buffer)
    headers = [
        'Semester', 'Course Number', 'Course Title', 'Professor',
        'TA Eagle ID', 'TA First Name', 'TA Last Name', 'TA Email'
    ]
    csv_writer.writerow(headers)

    try:
        csv_writer = write_ta_assignment_data(csv_writer, semester)
    except:
        csv_buffer.close()
        raise
    else:
        csv_buffer.seek(0)
        response = HttpResponse(csv_buffer, content_type='text/csv')
        response['Content-Disposition'] = \
            f'attachment; filename={semester}_TA_Assignment_Data.csv'
        return response


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
