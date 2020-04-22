from django import forms
from django.contrib.postgres.forms import JSONField
from .models import Profile
from .utils import get_semester_choices


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')


class SemesterForm(forms.Form):
    semester = forms.ChoiceField(choices=get_semester_choices)


class ApplicationForm(forms.Form):
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class ProfileForm(forms.Form):
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)


class LabHourConstraintsForm(forms.Form):
    semester = forms.CharField(widget=forms.HiddenInput(), required=False)
    lab_hour_data = JSONField(widget=forms.HiddenInput(), required=False)
