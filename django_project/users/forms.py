from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, get_user_model
from ta_system.models import Profile
from ta_system.validators import DataValidator
from ta_system.data_formats.applicant_data_formats \
    import DATA_FORMATS as APPILCANT_DATA_FORMATS
from .data_formats.user_data_formats \
    import DATA_FORMATS as USER_DATA_FORMATS


class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(max_length=30, label="BC Email",
        validators=[DataValidator(
            regex=USER_DATA_FORMATS['username'], 
            message="Please enter a valid BC email address."
        )]
    )
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()
        return user


class ProfileForm(forms.ModelForm):
    eagle_id = forms.CharField(max_length=8, label="Eagle ID",
        validators=[DataValidator(
            regex=APPILCANT_DATA_FORMATS['eagle_id'], 
            message="Please enter a valid 8-digit eagle id, e.g. '58704254'."
        )]
    )

    class Meta:
        model = Profile
        fields = ['eagle_id']
