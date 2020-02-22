from django import forms

class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')
