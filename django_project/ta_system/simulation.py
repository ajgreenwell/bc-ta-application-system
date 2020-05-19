from .models import Semester, SystemStatus
from .utils import get_current_semester, get_year_and_semester_code
from django.contrib import messages
from django.shortcuts import redirect


def get_courses_taken_prev(applicant):
    courses_taken = applicant.courses_taken.all()
    semester = get_year_and_semester_code(get_current_semester())
    current_semester = Semester.objects.get(
        year=semester[0], semester_code=semester[1])
    courses_taken_prev = []
    for course_taken in courses_taken:
        if course_taken.semester != current_semester:
            courses_taken_prev.append(course_taken)
    return courses_taken_prev


def assign_TA(applicant, course, num_tas):
    courses_taken = get_courses_taken_prev(applicant)
    for course_taken in courses_taken:
        if course.course_number[:8] == course_taken.course_number[:8]:
            if applicant.ta_assignments.all().count() == 0:
                num_tas = num_tas + 1
                course.teaching_assistants.add(applicant)
                applicant.ta_assignments.add(course)
    return num_tas


def assign_CS1_TA(applicant, course, col, row, lab_hour_preferences, num_tas):
    courses_taken = get_courses_taken_prev(applicant)
    if check_availability(col, row, lab_hour_preferences):
        for course_taken in courses_taken:
            if course_taken.course_number[:8] in ['CSCI1101', 'CSCI1103']:
                if applicant.ta_assignments.all().count() == 0:
                    num_tas = num_tas + 1
                    course.teaching_assistants.add(applicant)
                    applicant.ta_assignments.add(course)
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
    start_slot = int(4 * start_hour + start_min)

    end_hour = int(str_end[:2])
    end_min = int(str_end[3:5])
    if end_min % 15 == 0:
        end_min = end_min / 15
    else:
        end_min = end_min // 15 + 1
    end_slot = int(4 * end_hour + end_min)

    slotrange = int(end_slot - start_slot)
    for i in range(slotrange):
        row.append(start_slot + i)
    return row


def get_current_semester_preferences(lab_hour_preferences):
    current_semester = get_current_semester()
    for preference_object in lab_hour_preferences:
        if preference_object['semester'] == current_semester:
            return preference_object["preferences"]


def check_availability(cols, rows, lab_hour_preferences):
    availability = get_current_semester_preferences(lab_hour_preferences)
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
        messages.error(
            request, f'Lab is never open. Please specify hours of operation before running the simulation.')
        return redirect('admin:index')


def check_assignment(student, assignment_list, constraints, availability, qhour, day):
    if (assignment_list[qhour][day] == '' or assignment_list[qhour][day] == student.eagle_id) and \
            constraints[qhour][day] and availability[qhour][day] and \
            (assignment_list[qhour+1][day] == '' or assignment_list[qhour+1][day] == student.eagle_id) and \
            constraints[qhour+1][day] and availability[qhour+1][day] and \
            (assignment_list[qhour+2][day] == '' or assignment_list[qhour+2][day] == student.eagle_id) and \
            constraints[qhour+2][day] and availability[qhour+2][day] and \
            (assignment_list[qhour+3][day] == '' or assignment_list[qhour+3][day] == student.eagle_id) and \
            constraints[qhour+3][day] and availability[qhour+3][day]:
        return True
    return False


def assign_to_lab(current_semester, student, ta_availability):
    qhour_count = get_lab_qhours(current_semester, student)
    max_hrs = SystemStatus.objects.order_by('id').last().max_lab_hours_per_ta
    availability = get_current_semester_preferences(student.lab_hour_preferences)
    constraints = current_semester.lab_hour_constraints
    assignment_list = current_semester.lab_hour_assignments
    max_avail = max([max(x) for x in ta_availability])
    for num_avail_tas in range(1, max_avail+1):
        for day in range(7):
            quarterhour = 0
            while quarterhour < len(assignment_list) - 4:
                if qhour_count >= max_hrs * 4:
                    return
                if ta_availability[quarterhour][day] == num_avail_tas:
                    if check_assignment(student, assignment_list, constraints, availability, quarterhour, day):
                        for i in range(4):
                            if assignment_list[quarterhour+i][day] == student.eagle_id:
                                qhour_count -= 1
                            else:
                                assignment_list[quarterhour+i][day] = student.eagle_id
                        setattr(current_semester, 'lab_hour_assignment', assignment_list)
                        current_semester.save()
                        qhour_count += 4
                quarterhour += 1


def get_lab_qhours(current_semester, student):
    qhour_count = 0
    assignment_list = current_semester.lab_hour_assignments
    for day in range(7):
        for qhour in range(len(assignment_list)):
            if assignment_list[qhour][day] == student.eagle_id:
                qhour_count += 1
    return qhour_count


def create_ta_availability_matrix(current_semester, valid_applications):
    matrix = [[0 for x in range(7)] for n in range(4 * 24)]
    max_hrs = SystemStatus.objects.order_by('id').last().max_lab_hours_per_ta
    for app in valid_applications:
        if get_lab_qhours(current_semester, app.applicant) >= max_hrs*4:
            continue
        availability = get_current_semester_preferences(app.applicant.lab_hour_preferences)
        for day in range(7):
            for qhour in range(len(availability)):
                if availability[qhour][day]:
                    matrix[qhour][day] += 1
    return matrix


def is_schedule_full(current_semester):
    constraints = current_semester.lab_hour_constraints
    assignment_list = current_semester.lab_hour_assignments
    for day in range(7):
        for qhour in range(len(assignment_list)):
            if constraints[qhour][day]:
                if not assignment_list[qhour][day]:
                    return False
    return True
