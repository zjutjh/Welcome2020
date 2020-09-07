import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def person_id_validator(value):
    # 暂时只写了大陆二代身份证
    print(value)
    ID_compile = re.compile(r'([A-Za-z](\d{6})\(\d\))|(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X|x)$')
    if not ID_compile.match(value):
        raise ValidationError(u"身份证格式不正确")

