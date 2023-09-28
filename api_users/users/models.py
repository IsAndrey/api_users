from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy as _f

from .validators import username_validator
from .validators import CHECK_UNIQUE_SUBSCRIBE, CHECK_SELF_SUBSCRIBE


MAX_LENGTH_NAME = 150
MAX_LENGTH_MAIL = 254


class CharField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['blank'] = False
        kwargs['help_text'] = _f(
            'Required. {max_length} characters or fewer.',
            max_length=MAX_LENGTH_NAME
        )
        super().__init__(*args, **kwargs)


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=MAX_LENGTH_MAIL,
        unique=True,
        help_text=_f(
            'Required. {max_length} characters or fewer.',
            max_length=MAX_LENGTH_MAIL
        ),
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


class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors'
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    recipes_limit = models.PositiveSmallIntegerField(_('recipes limit'), default=0)

    class Meta:
        constraints = [
            CHECK_SELF_SUBSCRIBE,
            CHECK_UNIQUE_SUBSCRIBE
        ]
