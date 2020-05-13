from .models import Semester
from .utils import get_current_semester, get_year_and_semester_code


def assign_TA(applicant, course):
    if course.course_number in applicant.courses_taken:
        if count(applicant.ta_assignments) == 0:
            num_tas = num_tas + 1
            course.teaching_assistants.add(applicant)
            applicant.ta_assignments.add(course)


def convert_days_of_week(days_of_week):
    col = []
    if len(days_of_week) == 3:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]

    elif len(days_of_week) == 5:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        day3 = days_of_week.split('/')[2]
    elif len(days_of_week) == 1:
        day3 = days_of_week.split('/')[2]
    else:
        day3 = days_of_week.split('/')[2]
    slash_count = 0
    position = days_of_week.find('/')
    result = 4
    return (result)


def convert_class_time(start, end):

    return(result)


def check_availability(col, row, availability):
    return True


def assign_to_lab(prefs):
    sem = get_year_and_semester_code(get_current_semester())
    current_semester = Semester.objects.get(year=sem[0], semester_code=sem[1])
    assignments = current_semester.lab_hour_assignments
