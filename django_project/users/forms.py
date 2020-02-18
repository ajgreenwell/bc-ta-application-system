from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='BC Email'
    )

    eagleid = forms.IntegerField(
        label="Eagle ID",
        required=True,
    )

    class Meta:
        model = User
        fields = ['email', 'eagleid', 'password1', 'password2']
