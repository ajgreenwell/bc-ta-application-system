from .models import Semester
from .utils import get_current_semester, get_year_and_semester_code


def assign_TA(applicant, course):
    courses_taken = applicant.courses_taken.all()
    for course_taken in courses_taken:
        if course.course_number[:8] == course_taken.course_number[:8]:
            if applicant.ta_assignments.all().count() == 0:
                num_tas = num_tas + 1
                course.teaching_assistants.add(applicant)
                applicant.ta_assignments.add(course)


def assign_CS1_TA(applicant, course, col, row, lab_hour_preferences):
    courses_taken = applicant.courses_taken.all()
    if check_availability(col, row, lab_hour_preferences):
        for course_taken in courses_taken:
            if course_taken.course_number[:8] in ['CSCI1101', 'CSCI1103']:
                if applicant.ta_assignments.all().count() == 0:
                    num_tas = num_tas + 1
                    course.teaching_assistants.add(applicant)
                    applicant.ta_assignments.add(course)


def convert_day_to_number(day):
    if day == "S":
        return 0
    elif day == "M":
        return 1
    elif day == "T":
        return 2
    elif day == "M":
        return 3
    elif day == "R":
        return 4
    elif day == "F":
        return 5
    else:
        return 6


def convert_days_of_week(days_of_week):
    col = []
    if len(days_of_week) == 3:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
    elif len(days_of_week) == 5:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        day3 = days_of_week.split('/')[2]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
        col.append(convert_day_to_number(day3))
    else:
        col.append(convert_day_to_number(days_of_week))
    return (col)


def convert_class_time(start, end):
    row = []
    str_start = str(start)
    str_end = str(end)
    start_hour = int(str_start[:2])
    start_min = int(str_start[3:5])
    start_slot = 4 * start_hour + (start_min / 15)
    end_hour = int(str_end[:2])
    end_min = int(str_end[3:5])
    end_slot = 4 * end_hour + (end_min / 15)
    range = end_slot - start_slot
    for i in range:
        row.append(start_slot + 1)
    return(row)


def check_availability(cols, rows, lab_hour_preferences):
    availability = lab_hour_preferences["preferences"]
    for col in cols:
        for row in rows:
            if availability[row][col] == False:
                return False
    return True


def assign_to_lab(prefs):
    sem = get_year_and_semester_code(get_current_semester())
    current_semester = Semester.objects.get(year=sem[0], semester_code=sem[1])
    assignment_json = current_semester.lab_hour_assignments
    assignment_list = assignment_json['assignments']


def create_assignment_matrix():
    sem = get_year_and_semester_code(get_current_semester())
    current_semester = Semester.objects.get(year=sem[0], semester_code=sem[1])
    empty_matrix = [['' for x in range(7)] for n in range(4 * 24)]
    current_semester.lab_hour_assignments = {'assignments': empty_matrix}
