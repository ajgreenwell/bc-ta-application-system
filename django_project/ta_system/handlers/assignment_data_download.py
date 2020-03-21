from ..models import Semester
from csv import writer
from django.http import HttpResponse
from io import StringIO


def get_semester_choices():
    semesters = [str(semester) for semester in Semester.objects.all()]
    verbose_semesters = [get_verbose_semester(sem) for sem in semesters]
    semester_choices = list(zip(semesters, verbose_semesters))
    return sorted(semester_choices, key=lambda choice: choice[1], reverse=True)


def get_verbose_semester(semester):
    year = semester[:4]
    semester_code = semester[-1]
    verbose_semester = 'Spring' if semester_code == 'S' else 'Fall'
    return f'{year} {verbose_semester}'


def handle_assignment_data_download(semester):
    csv_buffer = StringIO()
    csv_writer = writer(csv_buffer)
    headers = [
        'Semester',
        'Course Number',
        'Course Title',
        'Professor',
        'TA Eagle ID',
        'TA First Name',
        'TA Last Name',
        'TA Email'
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
    num_unassigned_courses = 0
    courses = Semester.objects.get(semester=semester).course_set.all()
    for course in courses:
        tas = course.teaching_assistants.all()
        if not tas:
            num_unassigned_courses += 1
        for ta in tas:
            row = [
                course.semester,
                course.course_number,
                course.name,
                course.instructor.name,
                ta.eagle_id,
                ta.user.first_name,
                ta.user.last_name,
                ta.user.email
            ]
            csv_writer.writerow(row)
    if num_unassigned_courses == len(courses):
        raise ValueError(
            f'The semester ({get_verbose_semester(semester)}) has no ' +
            'courses to which any teaching assistants have been assigned'
        )
    return csv_writer
