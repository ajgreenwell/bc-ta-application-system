from django.shortcuts import render
from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from .models import Course, Instructor, CourseNumber
from .forms import UploadFileForm
from .handlers import handle_course_data_upload


class MyAdminSite(AdminSite):

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls = [path('', self.admin_view(self.index))] + urls
        return urls

    def index(self, request):
        app_list = self.get_app_list(request)
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list
        }
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_course_data_upload(request.FILES['file'])
                messages.success(request, 'File Uploaded Successfully.')
        else:
            form = UploadFileForm()

        request.current_app = self.name
        context['form'] = form.as_p()
        return render(request, 'admin/index.html', context)


admin_site = MyAdminSite()
admin_site.register(Course)
admin_site.register(Instructor)
admin_site.register(CourseNumber)
admin_site.register(User)




