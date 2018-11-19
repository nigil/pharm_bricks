import re
from django.core import validators
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ungettext


class PhoneValidator(validators.RegexValidator):
    regex = r'^[\d\s\-\+\(\)]+$'
    message = 'Please enter a valid phone number.'


class NameValidator(validators.RegexValidator):
    # to let all unicode letter symbols, dashes and space
    regex = r'^([^\W\d_]|[\- ])+$'
    message = 'Please use only letters, spaces and dash symbol.'
    flags = re.UNICODE


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ungettext(
                    "The password is too short, it must contain a minimum of %(min_length)d character.",
                    "The password is too short, it must contain a minimum of %(min_length)d characters.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("The password is too common."),
                code='password_too_common',
            )


class CustomNumericPasswordValidator(NumericPasswordValidator):
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("The password is entirely numeric."),
                code='password_entirely_numeric',
            )
