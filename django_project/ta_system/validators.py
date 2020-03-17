from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
import re


@deconstructible
class DataValidator():

    def __init__(self, regex=None, message=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message

    def __call__(self, value):
        data_format = re.compile(self.regex)
        if not data_format.fullmatch(str(value)):
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, DataValidator) and
            self.regex.pattern == other.regex.pattern and
            self.message == other.message
        )