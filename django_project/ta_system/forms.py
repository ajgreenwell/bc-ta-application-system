from django import forms
from django.contrib.postgres.forms import JSONField
from .models import Profile
from .handlers.assignment_data_download import get_semester_choices
from django.contrib.auth.models import User
from .validators import DataValidator
from .data_formats.applicant_data_formats \
    import DATA_FORMATS as APPILCANT_DATA_FORMATS
from users.data_formats.user_data_formats \
    import DATA_FORMATS as USER_DATA_FORMATS


class CourseDataUploadForm(forms.Form):
    file = forms.FileField(label='Course Data CSV')


class ApplicantDataUploadForm(forms.Form):
    file = forms.FileField(label='Applicant Data CSV')


class AssignmentDataDownloadForm(forms.Form):
    semester = forms.ChoiceField(choices=get_semester_choices)


class ApplicationForm(forms.Form):
    lab_hour_preferences = JSONField(
        widget=forms.HiddenInput(), required=False)


class LabHourPreferencesForm(forms.Form):
    lab_hour_preferences = JSONField(
        widget=forms.HiddenInput(), required=False)


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
