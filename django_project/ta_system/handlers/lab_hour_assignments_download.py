from ..models import Semester, Profile
from ..utils import get_verbose_semester
from .file_download import handle_file_download
from csv import writer
from django.http import HttpResponse
from io import StringIO
from ta_system.utils import get_year_and_semester_code

NUM_TIMESLOTS_PER_HOUR = 4


def handle_lab_hour_assignments_download(semester):
    headers = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Time of Day'
    ]
    def write_data(csv_writer):
        return write_lab_hour_assignment_data(csv_writer, semester)

    filename = f'{semester}_Lab_Hour_Assignments.csv'
    return handle_file_download(headers, write_data, filename)


def write_lab_hour_assignment_data(csv_writer, semester):
    semester_has_assigned_lab_hours = False
    year, semester_code = get_year_and_semester_code(semester)
    lab_hour_assignments = Semester.objects.get(
        year=year,
        semester_code=semester_code
    ).lab_hour_assignments
    for idx, row in enumerate(lab_hour_assignments):
        row_to_write = []
        for eagle_id in row:
            if eagle_id:
                semester_has_assigned_lab_hours = True
                name = Profile.objects.get(eagle_id=eagle_id).full_name
                row_to_write.append(name)
            else:
                row_to_write.append('-')
        if is_hour(idx):
            hour_string = get_hour_string(idx)
            row_to_write.append(hour_string)
        else:
            row_to_write.append('')
        csv_writer.writerow(row_to_write)
    if not semester_has_assigned_lab_hours:
        raise ValueError(
            f'The semester ({get_verbose_semester(semester)}) has no ' +
            'teaching assistants to which any lab hours have been assigned.'
        )
    last_row = ['' for _ in range(7)]
    last_row.append('12:00 AM')
    csv_writer.writerow(last_row)
    return csv_writer


def is_hour(idx):
    return idx % NUM_TIMESLOTS_PER_HOUR == 0


def get_hour_string(idx):
    hour = idx // NUM_TIMESLOTS_PER_HOUR
    if hour == 0:
        return '12:00 AM'
    if hour < 12:
        return f'{hour}:00 AM'
    else:
        return f'{hour - 12}:00 PM'
