from datetime import date
from .models import Application, Semester


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


def has_submitted_application(user):
    current_semester = Semester.objects.get(semester=get_current_semester())
    try:
        Application.objects.get(applicant=user, semester=current_semester)
    except:
        return False
    return True


def remove_preferences(student, semester):
    return [obj for obj in student.lab_hour_preferences \
            if obj['semester'] != semester]


def save_preferences(student, preferences):
    current_semester = get_current_semester()
    current_preferences = student.lab_hour_preferences
    if has_submitted_application(student.user):
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
            if col: return True
    return False


def get_constraints(semester):
    semester_obj = Semester.objects.get(semester=semester)
    return semester_obj.lab_hour_constraints


def save_constraints(semester, constraints):
    semester_obj = Semester.objects.get(semester=semester)
    semester_obj.lab_hour_constraints = constraints
    semester_obj.save()
