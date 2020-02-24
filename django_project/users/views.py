from django.shortcuts import render


def register(request):
    return render(request, 'users/register.html', {'title': 'Register'})


def login(request):
    return render(request, 'users/login.html', {'title': 'Login'})

