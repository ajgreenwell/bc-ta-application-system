from django.shortcuts import render, redirect
from .models import SystemStatus
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    date_list = SystemStatus.objects.order_by('id')
    date_list = date_list.reverse()
    status_dict = {
        'system_status': date_list,
        'last_system_status': date_list.first()
    }
    return render(request, 'ta_system/home.html', context=status_dict)
