from django.shortcuts import render, redirect


def home(request):
    return render(request, 'ta_system/home.html')
