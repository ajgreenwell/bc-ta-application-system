from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import dumps

from .handlers.bad_request import handle_bad_request
from .forms import ApplicationForm, LabHourPreferencesForm, UserUpdateForm, EagleIdForm
from .models import SystemStatus

import ta_system.utils as utils


@login_required
def home(request):
    if request.method not in ('GET', 'POST'):
        return handle_bad_request(request, app='ta_system', expected='GET, POST')

    context = {
        'system_is_open': SystemStatus.objects.order_by('id').last()
    }
    student = request.user.profile
    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            preferences = form.cleaned_data.get('lab_hour_data')
            if utils.is_valid_preferences(preferences):
                utils.save_preferences(student, preferences)
                context['user_has_submitted_application'] = True
            else:
                messages.error(
                    request,
                    'Error: Please specify which times you ' +
                    'would be available to tend the CS Lab.'
                )
    elif utils.has_submitted_application(student):
        context['user_has_submitted_application'] = True

    context['application_form'] = form
    return render(request, 'ta_system/home.html', context=context)


@login_required
def profile(request):
    if request.method not in ('GET', 'POST'):
        return handle_bad_request(request, app='ta_system', expected='GET, POST')

    user_form = UserUpdateForm(instance=request.user)
    preference_form = LabHourPreferencesForm()
    eagleid_form = EagleIdForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        preference_form = LabHourPreferencesForm(request.POST)
        eagleid_form = EagleIdForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and preference_form.is_valid() and eagleid_form.is_valid():
            user_form.save()
            eagleid_form.save()
            student = request.user.profile
            preferences = preference_form.cleaned_data.get(
                'lab_hour_data')
            if utils.is_valid_preferences(preferences):
                utils.save_preferences(student, preferences)
                messages.success(
                    request,
                    'Success! Your profile information has been saved.'
                )
                return redirect('ta_system:profile')
            else:
                messages.error(
                    request,
                    'Error: Please specify which times you ' +
                    'would be available to tend the CS Lab. '
                )
    context = {
        'user_form': user_form,
        'preference_form': preference_form,
        'eagleid_form': eagleid_form
    }
    return render(request, 'ta_system/profile.html', context=context)


@login_required
def get_lab_hour_preferences(request):
    if request.method != 'GET':
        return handle_bad_request(request, app='ta_system', expected='GET')

    student = request.user.profile
    semester = utils.get_current_semester()
    preferences = utils.get_preferences(student, semester)
    return HttpResponse(
        dumps(preferences),
        content_type='application/json',
        status=200
    )


@login_required
def get_lab_hour_constraints(request):
    if request.method != 'GET':
        return handle_bad_request(request, app='admin', expected_method='GET')

    semester = utils.get_current_semester()
    constraints = utils.get_constraints(semester)
    return HttpResponse(
        dumps(constraints),
        content_type='application/json',
        status=200
    )
