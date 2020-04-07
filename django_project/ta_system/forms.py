from django import forms
from .handlers.assignment_data_download import get_semester_choices


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')


class AssignmentDataDownloadForm(forms.Form):
    semester = forms.ChoiceField(choices=get_semester_choices)
