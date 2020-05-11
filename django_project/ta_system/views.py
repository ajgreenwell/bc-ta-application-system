from django.shortcuts import render, redirect
from .models import SystemStatus, Semester, Application, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import dumps

from .handlers.bad_request import handle_bad_request
from .forms import ApplicationForm
from .utils import get_current_semester
from django.contrib import messages
from .forms import ApplicationForm, ProfileForm
from .models import SystemStatus

import ta_system.utils as utils


@login_required
def home(request):

    if request.method not in ('GET', 'POST'):
        return handle_bad_request(request, app='ta_system', expected='GET, POST')

    app_form = ApplicationForm()
    context = {
        'system_is_open': SystemStatus.objects.order_by('id').last(),
        'app_form': app_form
    }

    user = request.user
    student = user.profile

    if request.method == 'POST':
        app_form = ApplicationForm(request.POST)
        if app_form.is_valid():
            semester = Semester.objects.get(semester=get_current_semester())
            course_preferences = [app_form.cleaned_data.get('course1'),
                                  app_form.cleaned_data.get('course2'),
                                  app_form.cleaned_data.get('course3')]
            instructor_preferences = [app_form.cleaned_data.get('prof1'),
                                      app_form.cleaned_data.get('prof2'),
                                      app_form.cleaned_data.get('prof3')]
            major = app_form.cleaned_data.get('major')
            grad_year = app_form.cleaned_data.get('grad_year')
            preferences = app_form.cleaned_data.get('lab_hour_data')
            if utils.is_valid_preferences(preferences):
                utils.save_preferences(student, preferences)
                context['user_has_submitted_application'] = True
            else:
                messages.error(
                    request,
                    'Error: Please specify which times you ' +
                    'would be available to tend the CS Lab.'
                )
            app = Application(applicant=user,
                              semester=semester,
                              course_preferences=course_preferences,
                              instructor_preferences=instructor_preferences,
                              major=major,
                              grad_year=grad_year)
            app.save()

            student = Profile.objects.get(user=user)
            messages.success(request, f'Application Submitted For {student.full_name}!')
            preferences = app_form.cleaned_data.get('lab_hour_data')
            utils.save_preferences(student, preferences)
            return redirect('ta_system:home')

    elif utils.has_submitted_application(user):
        context['user_has_submitted_application'] = True

    return render(request, 'ta_system/home.html', context=context)


@login_required
def profile(request):
    if request.method not in ('GET', 'POST'):
        return handle_bad_request(request, app='ta_system', expected='GET, POST')

    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            student = request.user.profile
            preferences = form.cleaned_data.get('lab_hour_data')
            if utils.is_valid_preferences(preferences):
                utils.save_preferences(student, preferences)
                messages.success(
                    request,
                    'Success! Your profile information has been saved.'
                )
            else:
                messages.error(
                    request,
                    'Error: Please specify which times you ' +
                    'would be available to tend the CS Lab.'
                )
    context = {'profile_form': form}
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
