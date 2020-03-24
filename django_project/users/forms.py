from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, get_user_model
from ta_system.models import Profile
from ta_system.validators import DataValidator


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']

        widgets = {
            'username': forms.EmailInput(attrs={
                'placeholder': 'BC Email',
            }),
            'email': forms.HiddenInput,
        }

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()
        return user


class ProfileForm(forms.ModelForm):
    eagle_id = forms.CharField(max_length=8, required=True,
        validators=[DataValidator(
            regex=APPILCANT_DATA_FORMATS['eagle_id'], 
            message="Please enter a valid 8-digit eagle id, e.g. '58704254'."
        )]
    )

    class Meta:
        model = Profile
        fields = ['eagle_id']
