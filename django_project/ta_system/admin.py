from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError as AlreadyExistsError
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html

from .handlers.bad_request import handle_bad_request
from .handlers.course_data_upload import handle_course_data_upload
from .handlers.applicant_data_upload import handle_applicant_data_upload
from .handlers.assignment_data_download import handle_assignment_data_download
from .handlers.file_upload import UPLOAD_DATA_FORMATS_URL as DATA_FORMATS_URL

import ta_system.html_utils as html
import ta_system.forms as forms
import ta_system.models as models


MAX_NUM_TO_DISPLAY = 3
UL_STYLE = "margin: 0 0 0 6px; padding-left: 6px;"


class CustomAdminSite(AdminSite):

    site_title = "Boston College TA Application System"
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
                 name='assignment_data_download'),
            path('change_system_status',
                 self.admin_view(self.change_system_status),
                 name='change_system_status')
        ] + urls
        return urls

    def index(self, request):
        app_list = self.get_app_list(request)
        status_list = models.SystemStatus.objects.order_by('id')
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            'course_data_upload_form': forms.CourseDataUploadForm(),
            'applicant_data_upload_form': forms.ApplicantDataUploadForm(),
            'assignment_data_download_form': forms.AssignmentDataDownloadForm(),
            'last_system_status': status_list.last()
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
                messages.error(
                    request, f'Applicant Data Upload Failed: {err}.')
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
                messages.success(
                    request, 'Applicant Data Uploaded Successfully.')
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

    def change_system_status(self, request):
        if request.method != 'POST':
            return handle_bad_request(request, app='admin', expected_method='POST')
        new_system_status = models.SystemStatus()
        if models.SystemStatus.objects.count() > 0:
            previous_system_status = models.SystemStatus.objects.order_by(
                'id').last()
            new_system_status.status = not previous_system_status.status
        else:
            new_system_status.status = True
        new_system_status.save()
        return redirect('admin:index')


class CourseAdmin(ModelAdmin):
    filter_horizontal = ('teaching_assistants',)
    list_filter = ('semester__semester', 'instructor__name')
    list_display_links = ('course_number', 'name')
    list_display = (
        'semester', 'course_number', 'name',
        'instructor', 'get_teaching_assistants'
    )
    fieldsets = (
        ('Assign TAs to this Course', {
            'fields': ('teaching_assistants',)
        }),
        ('Edit Course Information', {
            'fields': (
                'semester', 'course_number',
                'name', 'instructor',
                'days_of_week', 'start_time',
                'end_time', 'building',
                'room_number', 'max_num_tas'
            )
        })
    )

    class Media:
        css = {'all': ('admin/filter-horizontal-bug-fix.css',)}

    def display_ta(self, ta):
        return ta.full_name

    def get_teaching_assistants(self, obj):
        tas = obj.teaching_assistants.all()
        return html.generate_ul(
            model_objects=tas,
            display_func=self.display_ta,
            style=UL_STYLE
        )

    get_teaching_assistants.short_description = 'Teaching Assistants'


class ProfileAdmin(ModelAdmin):
    filter_vertical = ('courses_taken', 'ta_assignments')
    list_display = (
        'eagle_id', 'get_first_name', 'get_last_name',
        'get_email', 'get_ta_assignments'
    )
    list_display_links = ('eagle_id', 'get_first_name', 'get_last_name')
    fieldsets = (
        ('Select the Courses for which this Student is a TA', {
            'fields': ('ta_assignments',)
        }),
        ('Select which Courses this Student has Taken', {
            'fields': ('courses_taken',)
        }),
        ('Edit Student Information', {
            'fields': ('user', 'eagle_id', 'lab_hour_preferences')
        })
    )

    class Media:
        css = {'all': ('admin/filter-vertical-bug-fix.css',)}

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    def get_ta_assignments(self, obj):
        courses = obj.ta_assignments.all()
        return html.generate_ul(
            model_objects=courses,
            display_func=str,
            style=UL_STYLE,
            max_to_display=MAX_NUM_TO_DISPLAY
        )

    get_first_name.short_description = 'First Name'
    get_last_name.short_description = 'Last Name'
    get_email.short_description = 'Email'
    get_ta_assignments.short_description = 'TA Assignments'


class InstructorAdmin(ModelAdmin):
    fields = ('name', 'get_all_courses', 'get_all_teaching_assistants')
    readonly_fields = ('get_all_courses', 'get_all_teaching_assistants')
    list_display = ('name', 'get_courses')

    def get_tas_from_courses(self, courses):
        tas = []
        for course in courses:
            course_tas = course.teaching_assistants.all()
            for ta in course_tas:
                if ta not in tas:
                    tas.append(ta)
        return tas

    def get_courses(self, obj, display_func=str):
        courses = obj.course_set.all()
        return html.generate_ul(
            model_objects=courses,
            display_func=display_func,
            style=UL_STYLE,
            max_to_display=MAX_NUM_TO_DISPLAY
        )

    def get_all_courses(self, obj, display_func=str):
        courses = obj.course_set.all()
        ul_style = "margin: 0 0 0 0; padding-left: 0;"
        return html.generate_ul(
            model_objects=courses,
            display_func=display_func,
            style=ul_style
        )

    def get_all_teaching_assistants(self, obj):
        courses = obj.course_set.all()
        tas = self.get_tas_from_courses(courses)
        ul_style = "margin: 0 0 0 0; padding-left: 0;"
        return html.generate_ul(
            model_objects=tas,
            display_func=str,
            style=ul_style
        )

    get_courses.short_description = 'Courses'
    get_all_courses.short_description = 'Courses'
    get_all_teaching_assistants.short_description = 'Teaching Assistants'


class SemesterAdmin(InstructorAdmin):
    fields = ('semester', 'get_all_courses', 'get_all_teaching_assistants')
    readonly_fields = ('get_all_courses', 'get_all_teaching_assistants')
    list_display = ('semester', 'get_courses')

    def display_course(self, course):
        return course.course_number_and_name

    def get_courses(self, obj):
        return super().get_courses(obj, display_func=self.display_course)

    def get_all_courses(self, obj):
        return super().get_all_courses(obj, display_func=self.display_course)

    get_courses.short_description = 'Courses'
    get_all_courses.short_description = 'Courses'


class SystemStatusAdmin(ModelAdmin):
    list_display = ('id', 'status', 'date_changed')


admin_site = CustomAdminSite()
admin_site.register(models.User, UserAdmin)
admin_site.register(models.Course, CourseAdmin)
admin_site.register(models.Profile, ProfileAdmin)
admin_site.register(models.Instructor, InstructorAdmin)
admin_site.register(models.Semester, SemesterAdmin)
admin_site.register(models.SystemStatus, SystemStatusAdmin)
