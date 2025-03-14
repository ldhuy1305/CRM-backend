import re

from rest_framework.exceptions import ValidationError

from api import constants


def validate_password(password: str):
    reg = constants.REGEX_CHECK_FORMAT_PASSWORD
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if not mat:
        raise ValidationError(
            "The password must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, one digit, and one special character"
        )
