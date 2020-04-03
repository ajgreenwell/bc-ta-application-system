from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def register(request):
    user_form = UserRegisterForm()
    profile_form = ProfileForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            profile_form = ProfileForm(
                request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, f'Account Created For {username}!')
                return redirect('ta_system:home')
        else:
            messages.error(request, f'Please Correct The Error Below.')
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login(request):
    return render(request, 'users/login.html', {'title': 'Login'})
