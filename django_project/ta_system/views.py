from django.shortcuts import render, redirect
from .models import SystemStatus


def home(request):
    date_list = SystemStatus.objects.order_by('id')
    date_list = date_list.reverse()
    status_dict = {
        'system_status': date_list,
        'last_system_status': date_list.first()
    }
    return render(request, 'ta_system/home.html', context=status_dict)
