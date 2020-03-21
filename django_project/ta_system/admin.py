from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError as AlreadyExistsError
from django.shortcuts import render, redirect
from django.urls import path
from .handlers.bad_request import handle_bad_request
from .handlers.course_data_upload import handle_course_data_upload
from .handlers.applicant_data_upload import handle_applicant_data_upload
from .handlers.assignment_data_download import handle_assignment_data_download
import ta_system.models as models
import ta_system.forms as forms


class CustomAdminSite(AdminSite):

    site_title  = "Boston College TA Application System"
    site_header = "Boston College TA Application System"
    index_title = "System Admin"

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path('', self.admin_view(self.index)),
            path('course_data_upload', 
                self.admin_view(self.course_data_upload), 
                name='course_data_upload'),
            path('applicant_data_upload', 
                self.admin_view(self.applicant_data_upload), 
                name='student_data_upload'),
            path('assignment_data_download',
                self.admin_view(self.assignment_data_download),
                name='assignment_data_download')
        ] + urls
        return urls

    def index(self, request):
        app_list = self.get_app_list(request)
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            'course_data_upload_form': forms.CourseDataUploadForm(),
            'applicant_data_upload_form': forms.ApplicantDataUploadForm(),
            'assignment_data_download_form': forms.AssignmentDataDownloadForm()
        }
        request.current_app = self.name
        return render(request, 'admin/index.html', context)

    def course_data_upload(self, request):
        if request.method != 'POST':
            return handle_bad_request(request, app='admin', expected_method='POST')

        form = forms.CourseDataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_course_data_upload(request.FILES['file'])
            except TypeError as err:
                messages.error(request, f'Course Data Upload Failed: {err}.')
            except ValueError as err:
                messages.error(
                    request,
                    f'Course Data Upload Failed: The course {err} is duplicated ' +
                    'in your file. Please remove all duplicate courses and try again.'
                )
            except AlreadyExistsError as err:
                messages.error(
                    request,
                    f'Course Data Upload Failed: The course {err} already exists in our database. ' +
                    'If you wish to overwrite this course, delete it and try again.'
                )
            except Exception as err:
                messages.error(
                    request,
                    f'Course Data Eupload Failed: The following uncaught error occurred: {err}'
                )
            else:
                messages.success(request, 'Course Data Uploaded Successfully.')
        return redirect('admin:index')

    def applicant_data_upload(self, request):
        if request.method != 'POST':
            return handle_bad_request(request, app='admin', expected_method='POST')

        form = forms.ApplicantDataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_applicant_data_upload(request.FILES['file'])
            except TypeError as err:
                messages.error(request, f'Applicant Data Upload Failed: {err}.')
            except ObjectDoesNotExist as err:
                messages.error(
                    request,
                    f'Applicant Data Upload Failed: {err}. Please double check your data.'
                )
            except Exception as err:
                messages.error(
                    request,
                    f'Applicant Data Upload Failed: The following uncaught error occurred: {err}.'
                )
            else:
                messages.success(request, 'Applicant Data Uploaded Successfully.')
        return redirect('admin:index')

    def assignment_data_download(self, request):
        if request.method != 'GET':
            return handle_bad_request(request, app='admin', expected_method='GET')

        form = forms.AssignmentDataDownloadForm(request.GET)
        if form.is_valid():
            semester = form.cleaned_data.get('semester')
            try:
                response = handle_assignment_data_download(semester)
                return response
            except ValueError as err:
                messages.error(
                    request,
                    f'TA Assignment Data Download Failed: {err}.'
                )
        return redirect('admin:index')


class CourseAdmin(ModelAdmin):
    filter_vertical = ('teaching_assistants',)


class ProfileAdmin(ModelAdmin):
    filter_vertical = ('courses_taken', 'ta_assignments')


admin_site = CustomAdminSite()
admin_site.register(models.User, UserAdmin)
admin_site.register(models.Profile, ProfileAdmin)
admin_site.register(models.Course, CourseAdmin)
admin_site.register(models.Semester)
admin_site.register(models.Instructor)
