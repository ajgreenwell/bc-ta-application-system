DATA_FORMATS = {
    'semester': '\d{4}[FS]',
    'course_number': '[A-Z]{4}\d{6}',
    'name': '\S+( \S+)*',
    'instructor': '\S+( \S+)*',
    'days_of_week': '[MTWRFAS](/[MTWRFAS])*',
    'start_time': '\d{2}:\d{2}(:\d{2})*',
    'end_time': '\d{2}:\d{2}(:\d{2})*',
    'building': '\S+( \S+)*',
    'room_number': '\d+[A-Z]{0,1}',
    'max_num_tas': '\d+'
}
EXPECTED_LINE_FORMAT = ','.join(DATA_FORMATS.values())
