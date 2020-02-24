from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def register(request):
    return render(request, 'users/register.html', {'title', 'Register'})


def login(request):
    return render(request, 'users/login.html', {'title': 'Login'})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
