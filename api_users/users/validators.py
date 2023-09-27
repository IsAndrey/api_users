import re

from rest_framework.exceptions import ValidationError
from django.db.models import CheckConstraint, Q, F, UniqueConstraint
from django.utils.translation import gettext_lazy as _


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

class CheckEqualFieldsValidator():
    """
    Проверка совпадения значения полей сериализатора. Не нужен.
    """
    message = _('Поля {field_names} Не должны совпадать.')
    missing_message = _('This field is required.')
    requires_context = True

    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)

        # Ignore validation if any field is None
        checked_values = [
            value for field, value in attrs.items() if (field in self.fields) and (value is not None)
        ]
        # Добавить условие на максимальное вхождение в checked_values больше 1
        field_names = ', '.join(self.fields)
        message = self.message.format(field_names=field_names)
        raise ValidationError(message, code='unique')

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
