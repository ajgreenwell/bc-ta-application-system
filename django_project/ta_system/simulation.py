from .models import Semester, SystemStatus
from .utils import get_current_semester, get_year_and_semester_code
from django.contrib import messages
from django.shortcuts import redirect


def assign_TA(applicant, course, num_tas):
    courses_taken = applicant.courses_taken.all()
    for course_taken in courses_taken:
        if course.course_number[:8] == course_taken.course_number[:8]:
            if applicant.ta_assignments.all().count() == 0:
                num_tas = num_tas + 1
                course.teaching_assistants.add(applicant)
                applicant.ta_assignments.add(course)
                print('*********' + course.name + course.course_number + ": " +
                      applicant.user.username)
    return num_tas


def assign_CS1_TA(applicant, course, col, row, lab_hour_preferences, num_tas):
    courses_taken = applicant.courses_taken.all()
    if check_availability(col, row, lab_hour_preferences):
        for course_taken in courses_taken:
            if course_taken.course_number[:8] in ['CSCI1101', 'CSCI1103']:
                if applicant.ta_assignments.all().count() == 0:
                    num_tas = num_tas + 1
                    course.teaching_assistants.add(applicant)
                    applicant.ta_assignments.add(course)
                    print('*********' + course.name + course.course_number + ": " +
                          applicant.user.username)
    return num_tas


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
    if len(days_of_week) == 1:
        col.append(convert_day_to_number(days_of_week))
    elif len(days_of_week) == 3:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
    else:
        day1 = days_of_week.split('/')[0]
        day2 = days_of_week.split('/')[1]
        day3 = days_of_week.split('/')[2]
        col.append(convert_day_to_number(day1))
        col.append(convert_day_to_number(day2))
        col.append(convert_day_to_number(day3))
    return (col)


def convert_class_time(start, end):
    row = []
    str_start = str(start)
    str_end = str(end)

    start_hour = int(str_start[:2])
    start_min = int(str_start[3:5])
    if start_min % 15 == 0:
        start_min = start_min / 15
    else:
        start_min = start_min // 15 + 1
    start_slot = 4 * start_hour + start_min

    end_hour = int(str_end[:2])
    end_min = int(str_end[3:5])
    if end_min % 15 == 0:
        end_min = end_min / 15
    else:
        end_min = end_min // 15 + 1
    end_slot = 4 * end_hour + end_min

    slotrange = end_slot - start_slot
    for i in range(slotrange):
        row.append(start_slot + 1)
    return row


def check_availability(cols, rows, lab_hour_preferences):
    availability = lab_hour_preferences["preferences"]
    for col in cols:
        for row in rows:
            if availability[row][col] == False:
                return False
    return True


def check_sem_assignment(current_semester):
    if not current_semester.lab_hour_assignments:
        empty_matrix = [['' for x in range(7)] for n in range(4 * 24)]
        setattr(current_semester, 'lab_hour_assignments', empty_matrix)
        current_semester.save()


def check_sem_constraints(request, current_semester):
    if not current_semester.lab_hour_constraints:
        messages.error(request, f'Lab is never open. Please specify hours of operation before running the simulation.')
        return redirect('admin:index')


def assign_to_lab(current_semester, student):
    availability = student.lab_hour_preferences[0]['preferences']
    constraints = current_semester.lab_hour_constraints
    assignment_list = current_semester.lab_hour_assignments
    max_hrs = SystemStatus.objects.order_by('id').last().max_lab_hours_per_ta
    qhour_count = 0
    for day in range(7):
        for quarterhour in range(len(assignment_list)):
            if qhour_count >= max_hrs*4:
                return
            if assignment_list[quarterhour][day] == '':
                if constraints[quarterhour][day]:
                    if availability[quarterhour][day]:
                        assignment_list[quarterhour][day] = student.eagle_id
                        setattr(current_semester, 'lab_hour_assignment', assignment_list)
                        current_semester.save()
                        qhour_count += 1


def is_schedule_full(current_semester):
    constraints = current_semester.lab_hour_constraints
    assignment_list = current_semester.lab_hour_assignments
    for day in range(7):
        for qhour in range(len(assignment_list)):
            if constraints[qhour][day]:
                if not assignment_list[qhour][day]:
                    return False
    return True
