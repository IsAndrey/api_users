import re

from django.db.models import CheckConstraint, Q, F, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy as _f
from django.templatetags.static import static
from rest_framework.exceptions import ValidationError


REGEX_FOR_USERNAME = r'^[\w.@+-]+\Z'
DEFAULT_LIST_LIMIT = 10
DEFAULT_COOKING_TIME = 1
LENGTH_NAME_150 = 150
LENGTH_NAME_200 = 200
LENGTH_MAIL_254 = 254
MAX_LENGTH_SLUG = 200
LENGTH_COLOR_07 = 7
LENGTH_COLOR_03 = 3


# Проверка уникальности подписки.
CHECK_UNIQUE_SUBSCRIBE = UniqueConstraint(
    fields=['author', 'follower'],
    name=_('unique subscribe')
)

# Проверка подписки на самого себя.
CHECK_SELF_SUBSCRIBE = CheckConstraint(
    check=~Q(author__exact=F('follower')),
    name=_('check self subscribe')
)

# Проверка уникальности рецепта.
CHECK_UNIQUE_RECIPE = UniqueConstraint(
    fields=['user', 'recipe'],
    name=_('unique recipe')
)

def color_validator(value):
    ...

def cooking_time_validator(value):
    if value < DEFAULT_COOKING_TIME:
        raise ValidationError(_f(
            'The cooking time should not be less than {value}.',
            value=value
            ),
            _('not correct cooking time')
        )

def default_recipe_image():
    return static('images/default_recipe.jpg')

def default_name():
    return ''

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
            'The character {char} in the string {s_value} does not match the pattern {regex}.',  # noqa
            char=char, s_value=s_value, reqex=regex
            ),
            code
        )

def username_validator(value):
    """Проверка имени пользователя."""
    regex_validator(value, REGEX_FOR_USERNAME, _('not correct username'))
