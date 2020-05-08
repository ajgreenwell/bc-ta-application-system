from django import forms
from .handlers.assignment_data_download import get_semester_choices
from .models import Course, Semester, Instructor, Application
from .utils import get_current_semester
from datetime import date


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')


class AssignmentDataDownloadForm(forms.Form):
    semester = forms.ChoiceField(choices=get_semester_choices)


class ApplicationForm(forms.Form):

    def get_grad_years():
        year = date.today().year
        grad_years = [(year, str(year))]
        for i in range(4):
            year += 1
            grad_years.append((year, str(year)))
        return grad_years

    current_semester = Semester.objects.get(semester=get_current_semester())
    current_courses = list(Course.objects.filter(semester=current_semester).values_list('name', flat=True).distinct())
    course_choices = [('', 'No preference')]
    for course in current_courses:
        if (course, course) in course_choices:
            continue
        course_choices.append((course, course))

    prof_choices = [('', 'No preference')]
    prof_ids = list(Course.objects.filter(semester=current_semester).values_list('instructor', flat=True).distinct())
    profs = []
    for prof in prof_ids:
        profs.append(Instructor.objects.get(id=prof))
    for prof in profs:
        if (prof, prof) in prof_choices:
            continue
        prof_choices.append((prof, prof))

    year_choices = get_grad_years()

    course1 = forms.ChoiceField(choices=course_choices, required=False, label='Course 1')
    course2 = forms.ChoiceField(choices=course_choices, required=False, label='Course 2')
    course3 = forms.ChoiceField(choices=course_choices, required=False, label='Course 3')
    prof1 = forms.ChoiceField(choices=prof_choices, required=False, label='Professor 1')
    prof2 = forms.ChoiceField(choices=prof_choices, required=False, label='Professor 2')
    prof3 = forms.ChoiceField(choices=prof_choices, required=False, label='Professor 3')
    major = forms.CharField(max_length=200, label='Major(s)')
    grad_year = forms.ChoiceField(choices=year_choices, label='Graduation Year')
