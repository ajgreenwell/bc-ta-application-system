from colorsys import hsv_to_rgb
from datetime import date
from .models import Application, Semester


def get_year_and_semester_code(semester):
    return (semester[:4], semester[-1])


def get_semester_choices():
    semesters = [str(semester) for semester in Semester.objects.all()]
    verbose_semesters = [get_verbose_semester(sem) for sem in semesters]
    return list(zip(semesters, verbose_semesters))


def get_verbose_semester(semester):
    year = semester[:4]
    semester_code = semester[-1]
    verbose_semester = 'Spring' if semester_code == 'S' else 'Fall'
    return f'{year} {verbose_semester}'


def get_current_semester():
    spring_application_months = [10, 11, 12, 1, 2]
    today = date.today()
    year = str(today.year)
    if today.month in spring_application_months:
        return f'{year}S'
    return f'{year}F'


def get_preferences(student, semester):
    for obj in student.lab_hour_preferences:
        if obj['semester'] == semester:
            return obj['preferences']
    return None


def has_submitted_application(student):
    current_semester = get_current_semester()
    year, semester_code = get_year_and_semester_code(current_semester)
    semester = Semester.objects.get(year=year, semester_code=semester_code)
    try:
        Application.objects.get(applicant=student, semester=semester)
    except:
        return False
    return True


def remove_preferences(student, semester):
    return [obj for obj in student.lab_hour_preferences
            if obj['semester'] != semester]


def save_preferences(student, preferences):
    current_semester = get_current_semester()
    current_preferences = remove_preferences(student, current_semester)

    current_preferences.append({
        'semester': current_semester,
        'preferences': preferences
    })
    student.lab_hour_preferences = current_preferences
    student.save()


def is_valid_preferences(preferences):
    for row in preferences:
        for col in row:
            if col:
                return True
    return False


def get_constraints(semester):
    year, semester_code = get_year_and_semester_code(semester)
    semester_obj = Semester.objects.get(
        year=year,
        semester_code=semester_code
    )
    return semester_obj.lab_hour_constraints


def save_constraints(semester, constraints):
    year, semester_code = get_year_and_semester_code(semester)
    semester_obj = Semester.objects.get(year=year, semester_code=semester_code)
    semester_obj.lab_hour_constraints = constraints
    semester_obj.save()


def save_assignments(semester, assignments):
    year, semester_code = get_year_and_semester_code(semester)
    semester_obj = Semester.objects.get(year=year, semester_code=semester_code)
    semester_obj.lab_hour_assignments = assignments
    semester_obj.save()


def get_tas_from_courses(courses):
    tas = []
    for course in courses:
        course_tas = course.teaching_assistants.all()
        for ta in course_tas:
            if ta not in tas:
                tas.append(ta)
    return tas


def get_tas_from_semester(semester):
    tas = {}
    year, semester_code = get_year_and_semester_code(semester)
    semester_obj = Semester.objects.get(year=year, semester_code=semester_code)
    applications = Application.objects.filter(semester=semester_obj).all()
    for app in applications:
        ta = app.applicant
        tas[ta.eagle_id] = ta.full_name
    return tas


def get_ta_rgb_colors(tas):
    num_tas = len(tas)
    rgb_colors = []
    for i in range(num_tas):
        hue = calculate_hue_excluding_reds(i, num_tas)
        rgb_percentages = hsv_to_rgb(hue, .35, .96)
        rgb_values = [percent * 255 for percent in rgb_percentages]
        rgb_colors.append(rgb_values)
    return dict(zip(tas.keys(), rgb_colors))


def calculate_hue_excluding_reds(idx, num_tas):
    lower_bound = .1
    upper_bound = .9
    return lower_bound + (idx * (upper_bound - lower_bound) / num_tas)
