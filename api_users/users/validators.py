import re

from rest_framework.exceptions import ValidationError


REGEX_FOR_USERNAME = r'^[\w.@+-]+\Z'

def regex_validator(value, regex, code=''):
    """Проверка на соответствие регулярному выражению."""
    s_value = str(value)
    re_compile = re.compile(regex)
    if not re_compile.search(s_value):
        for i in range(len(s_value)):
            char = s_value[i]
            if not re_compile.search(char):
                break
        raise ValidationError(
            f'Символ {char} в '
            f'строке {s_value} не соответствует '
            f'шаблону {regex}',
            code
        )

def username_validator(value):
    """Проверка имени пользователя."""
    regex_validator(value, REGEX_FOR_USERNAME, 'not_correct_username')
