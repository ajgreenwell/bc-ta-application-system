from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            eagle_id = profile_form.cleaned_data.get('eagle_id')
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account Created For {username}!')
            return redirect('ta_system:home')
        else:
            messages.error(request, f'Please Correct The Error Below.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login(request):
    return render(request, 'users/login.html', {'title': 'Login'})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
