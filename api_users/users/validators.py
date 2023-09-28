import re

from rest_framework.exceptions import ValidationError
from django.db.models import CheckConstraint, Q, F, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy as _f


REGEX_FOR_USERNAME = r'^[\w.@+-]+\Z'


# Проверка уникальности подписки.
CHECK_UNIQUE_SUBSCRIBE = UniqueConstraint(
    fields=['author', 'follower'],
    name='unique_subscribe'
)

# Проверка подписки на самого себя.
CHECK_SELF_SUBSCRIBE = CheckConstraint(
    check=~Q(author__exact=F('follower')),
    name='check_self_subscribe'
)

def regex_validator(value, regex, code=''):
    """Проверка на соответствие регулярному выражению."""
    s_value = str(value)
    re_compile = re.compile(regex)
    if not re_compile.search(s_value):
        for i in range(len(s_value)):
            char = s_value[i]
            if not re_compile.search(char):
                break
        raise ValidationError(_f(
            'The character {char} in the string {s_value} does not match the pattern {regex}',  # noqa
            char=char, s_value=s_value, reqex=regex
            ),
            code
        )

def username_validator(value):
    """Проверка имени пользователя."""
    regex_validator(value, REGEX_FOR_USERNAME, 'not_correct_username')
