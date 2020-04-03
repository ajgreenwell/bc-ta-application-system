from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import loads
from .handlers.bad_request import handle_bad_request

import ta_system.utils as utils


@login_required
def home(request):
    if request.method not in ('GET', 'POST'):
        return handle_bad_request(request, app='ta_system', expected='GET, POST')

    student = request.user.profile
    if request.method == 'POST':
        preferences = loads(request.body)['lab_hour_preferences']
        utils.save_preferences(student, preferences)
        return HttpResponse(status=200)

    context = {}
    if utils.has_submitted_application(student):
        context['user_has_submitted_application'] = True
    return render(request, 'ta_system/home.html', context=context)


@login_required
def profile(request):
    return render(request, 'ta_system/profile.html')
