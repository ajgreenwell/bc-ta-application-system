from django import forms
from .models import Course, Semester, Instructor
from .utils import get_current_semester
from datetime import date
from django.contrib.postgres.forms import JSONField
from .models import Profile
from django.contrib.auth.models import User
from .validators import DataValidator
from .data_formats.applicant_data_formats \
    import DATA_FORMATS as APPILCANT_DATA_FORMATS
from users.data_formats.user_data_formats \
    import DATA_FORMATS as USER_DATA_FORMATS
from .utils import get_semester_choices


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')


class SemesterForm(forms.Form):
    semester = forms.ChoiceField(choices=get_semester_choices)


class ApplicationForm(forms.Form):

    def get_grad_years():
        year = date.today().year
        grad_years = [(year, str(year))]
        for i in range(4):
            year += 1
            grad_years.append((year, str(year)))
        return grad_years

    course_choices = [('', 'No preference')]
    current_semester = Semester.objects.get(year=get_current_semester()[:4], semester_code=get_current_semester()[-1])
    current_courses = list(Course.objects.filter(semester=current_semester).values_list('name', flat=True).distinct())
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
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class LabHourPreferencesForm(forms.Form):
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class LabHourConstraintsForm(forms.Form):
    semester = forms.CharField(widget=forms.HiddenInput(), required=False)
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class AssignLabHoursForm(forms.Form):
    semester = forms.CharField(widget=forms.HiddenInput(), required=False)
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class EagleIdForm(forms.ModelForm):
    eagle_id = forms.CharField(max_length=8, label="Eagle ID",
                               validators=[DataValidator(
                                   regex=APPILCANT_DATA_FORMATS['eagle_id'],
                                   message="Please enter a valid 8-digit eagle id, e.g. '58704254'."
                               )]
                               )

    class Meta:
        model = Profile
        fields = ['eagle_id']


class UserUpdateForm(forms.ModelForm):
    username = forms.EmailField(max_length=30, label="BC Email",
                                validators=[DataValidator(
                                    regex=USER_DATA_FORMATS['username'],
                                    message="Please enter a valid BC email address."
                                )])
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()
        return user
