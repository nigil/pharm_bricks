import re
from django.core import validators


class PhoneValidator(validators.RegexValidator):
    regex = r'^[\d\s\-\+\(\)]+$'
    message = 'Enter a valid phone number'


class NameValidator(validators.RegexValidator):
    # to let all unicode letter symbols, dashes and space
    regex = r'^([^\W\d_]|[\- ])+$'
    message = 'You can use only letters, spaces and dash symbol'
    flags = re.UNICODE
