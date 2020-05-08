from django.shortcuts import render, redirect
from .models import SystemStatus, Semester, Application, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import loads
from .handlers.bad_request import handle_bad_request
from .forms import ApplicationForm
from .utils import get_current_semester
from django.contrib import messages
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
            app = Application(applicant=user,
                              semester=semester,
                              course_preferences=course_preferences,
                              instructor_preferences=instructor_preferences,
                              major=major,
                              grad_year=grad_year)
            app.save()

            student = Profile.objects.get(eagle_id=user.eagle_id)
            messages.success(request, f'Application Submitted For {student.full_name}!')
            preferences = app_form.cleaned_data.get('lab_hour_data')
            utils.save_preferences(student, preferences)
            return redirect('ta_system:home')

    if utils.has_submitted_application(user):
        context['user_has_submitted_application'] = True
    return render(request, 'ta_system/home.html', context=context)


@login_required
def profile(request):
    return render(request, 'ta_system/profile.html')
