from ..models import Semester
from ..utils import get_verbose_semester
from csv import writer
from django.http import HttpResponse
from io import StringIO
from ta_system.utils import get_year_and_semester_code


def handle_file_download(headers, write_func, filename):
    csv_buffer = StringIO()
    csv_writer = writer(csv_buffer)
    csv_writer.writerow(headers)
    try:
        csv_writer = write_func(csv_writer)
    except:
        csv_buffer.close()
        raise
    else:
        csv_buffer.seek(0)
        response = HttpResponse(csv_buffer, content_type='text/csv')
        response['Content-Disposition'] = \
            f'attachment; filename={filename}'
        return response
