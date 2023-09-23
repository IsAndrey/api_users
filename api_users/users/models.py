from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import username_validator


MAX_LENGTH_NAME = 150
MAX_LENGTH_MAIL = 254

class CharField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['help_text'] = _(f'Required. {MAX_LENGTH_NAME} characters or fewer.')
        super().__init__(*args, **kwargs)

class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
            max_length=MAX_LENGTH_MAIL,
        unique=True,
        help_text=_(f'Required. {MAX_LENGTH_MAIL} characters or fewer.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    username = CharField(
        _('username'),
        max_length=MAX_LENGTH_NAME,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = CharField(_('first name'), max_length=MAX_LENGTH_NAME)
    last_name = CharField(_('last name'), max_length=MAX_LENGTH_NAME)
    password = CharField(_('password'), max_length=MAX_LENGTH_NAME)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
