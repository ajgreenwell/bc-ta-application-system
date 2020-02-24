from django.shortcuts import render


def home(request):
    return render(request, 'ta_system/home.html')

