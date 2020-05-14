DATA_FORMATS = {
    'semester': '\d{4}[FS]',
    'last_name': '.+',
    'first_name': '.+',
    'username': '\S+',
    'eagle_id': '\d{8}',
    'course_number': '[A-Z]{4}\d{6}',
    'course_title': '.+'
}
EXPECTED_LINE_FORMAT = ','.join(DATA_FORMATS.values())
