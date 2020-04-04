from datetime import date


def get_current_semester():
    spring_application_months = [10, 11, 12, 1, 2]
    today = date.today()
    year = str(today.year)
    if today.month in spring_application_months:
        return f'{year}S'
    return f'{year}F'


def save_preferences(student, preferences):
    new_preferences = {
        'semester': get_current_semester(),
        'preferences': preferences
    }
    student.lab_hour_preferences.append(new_preferences)
    student.save()


def has_submitted_application(student):
    current_semester = get_current_semester()
    semesters = [obj[0] for obj in student.lab_hour_preferences]
    return current_semester in semesters
