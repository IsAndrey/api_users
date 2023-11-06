from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy as _f

from .validators import (
    CHECK_UNUQUE_INGRIDIENT, CHECK_SELF_SUBSCRIBE, CHECK_UNIQUE_SUBSCRIBE,
    CHECK_UNIQUE_FAVORITE, CHECK_UNIQUE_SHOPPING, DEFAULT_AMOUNT,
    DEFAULT_COOKING_TIME, LENGTH_COLOR_07, LENGTH_MAIL_254, LENGTH_NAME_150,
    LENGTH_NAME_200,
    amount_validator, color_validator, cooking_time_validator,
    default_name, username_validator
)


class CharField150(models.CharField):
    """Текстовое поле длиной 150 символов."""
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = LENGTH_NAME_150
        kwargs['default'] = default_name
        kwargs['help_text'] = _f(
            'Required. {max_length} characters or fewer.',
            max_length=LENGTH_NAME_150
        )
        super().__init__(*args, **kwargs)


class CharField200(models.CharField):
    """Текстовое поле длиной 200 символов."""
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = LENGTH_NAME_200
        kwargs['default'] = default_name
        kwargs['help_text'] = _f(
            'Required. {max_length} characters or fewer.',
            max_length=LENGTH_NAME_200
        )
        super().__init__(*args, **kwargs)


class User(AbstractUser):
    """Пользователи."""
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_f(
            'Required. {max_length} characters or fewer.',
            max_length=LENGTH_MAIL_254
        ),
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    username = CharField150(
        _('username'),
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = CharField150(_('first name'))
    last_name = CharField150(_('last name'))
    password = CharField150(_('password'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscribe',
        through_fields=('follower', 'author')
    )


class Subscribe(models.Model):
    """Подписки."""
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

    class Meta:
        constraints = [
            CHECK_SELF_SUBSCRIBE,
            CHECK_UNIQUE_SUBSCRIBE
        ]


class NameList(models.Model):
    """Абстрактный список наименований."""
    name = CharField200(_('name'))

    class Meta:
        abstract = True


class Tag(NameList):
    """Тэги."""
    slug = models.SlugField(
        _('slug'), max_length=LENGTH_NAME_200, unique=True
    )
    color = models.CharField(
        _('color'), max_length=LENGTH_COLOR_07, validators=[color_validator]
    )


class Ingridient(NameList):
    """Ингридиенты."""
    measurement_unit = CharField200(_('measurement unit'))


class Recipe(NameList):
    """Рецепты."""
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to=Tag)
    ingridients = models.ManyToManyField(
        to=Ingridient, through='RecipeIngridient'
    )
    text = CharField200(_('text'))
    cooking_time = models.SmallIntegerField(
        default=DEFAULT_COOKING_TIME,
        validators=[cooking_time_validator]
    )
    image = models.ImageField(upload_to='recipes/images/')


class RecipeIngridient(models.Model):
    """Ингридиенты в рецептах."""
    ingridient = models.ForeignKey(
        to=Ingridient,
        on_delete=models.CASCADE,
        related_name='ingridients'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.SmallIntegerField(
        _('amount'), default=DEFAULT_AMOUNT, validators=[amount_validator]
    )

    class Meta:
        constraints = [CHECK_UNUQUE_INGRIDIENT]


class UserRecipe(models.Model):
    """Абстрактный список рецептов пользователя."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ShoppingCart(UserRecipe):
    """Корзина покупок."""

    class Meta:
        constraints = [
            CHECK_UNIQUE_SHOPPING
        ]


class FavoriteList(UserRecipe):
    """Любимые рецепты."""

    class Meta:
        constraints = [
            CHECK_UNIQUE_FAVORITE
        ]
