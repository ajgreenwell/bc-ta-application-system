from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Course, Instructor
from .forms import UploadFileForm
from .handlers import handle_course_data_upload, handle_bad_request


class MyAdminSite(AdminSite):

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls = [
            path('', self.admin_view(self.index)),
            path('course_data_upload', self.admin_view(self.course_data_upload), name='course_data_upload')
            ] + urls
        return urls

    def index(self, request):
        app_list = self.get_app_list(request)
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            'form': UploadFileForm()
        }
        request.current_app = self.name
        return render(request, 'admin/index.html', context)

    def course_data_upload(self, request):
        if request.method != 'POST':
            return handle_bad_request(request, app='admin', expected_method='POST')

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_course_data_upload(request.FILES['file'])
            except TypeError as err:
                messages.error(request, f'File Upload Failed: {err}')
            except IntegrityError as err:
                messages.error(request, f'File Upload Failed: One or more courses already exists. ' +
                                        'Please delete all courses before uploading new course data.')
            else:
                messages.success(request, 'File Uploaded Successfully.')
        return redirect('admin:index')


admin_site = MyAdminSite()
admin_site.register(Course)
admin_site.register(Instructor)
admin_site.register(User)




