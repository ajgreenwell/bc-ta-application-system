from django import forms


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class StudentDataUploadForm(forms.Form):
    file = forms.FileField(label='Student Data CSV')
