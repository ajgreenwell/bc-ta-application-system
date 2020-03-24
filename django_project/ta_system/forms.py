from django import forms


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')
