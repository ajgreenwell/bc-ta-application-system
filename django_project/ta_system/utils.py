from datetime import date


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


# THIS MUST BE CHANGED TO TEST FOR SOMETHING MORE 
# STABLE ONCE THE APPLICATION FORM IS FINISHED, BECAUSE
# STUDENTS CAN UPDATE LAB HOUR PREFERENCES FROM THEIR 
# PROFILE BEFORE SUBMITTING AN APPLICATION.
def has_submitted_application(student):
    current_semester = get_current_semester()
    semesters = [obj['semester'] for obj in student.lab_hour_preferences]
    return current_semester in semesters


def remove_preferences(student, semester):
    return [obj for obj in student.lab_hour_preferences \
            if obj['semester'] != semester]


def save_preferences(student, preferences):
    current_semester = get_current_semester()
    current_preferences = student.lab_hour_preferences
    if has_submitted_application(student):
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
