from ..utils.file_uploads import get_timestamped_fname, handle_file_upload


def handle_student_data_upload(file):
    fname = get_timestamped_fname('Student_Data', 'csv')
    handle_file_upload(
        file=file,
        destination=f'ta_system/static/student_data/{fname}',
        process_data_callback=process_student_data
    )


def process_student_data(fname):
    with open(fname, 'r') as students:
        validate_all_students(students)
        for student in students:
            process_student(student.split(','))


def validate_all_students(file):
    pass


def process_student(student_data):
    pass