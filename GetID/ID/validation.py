import re
from django.core.exceptions import ValidationError


def name_validator(value):
    if len(value) > 30 or len(value) <= 0:
        raise ValidationError(u"姓名格式不正确")


def person_id_validator(value):
    if len(value) > 50 or len(value) <= 0:
        raise ValidationError(u"身份证格式不正确")
