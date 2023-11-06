from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy as _f

from .validators import (
    CHECK_UNUQUE_INGRIDIENT, CHECK_SELF_SUBSCRIBE, CHECK_UNIQUE_SUBSCRIBE,
    CHECK_UNIQUE_FAVORITE, CHECK_UNIQUE_SHOPPING, DEFAULT_AMOUNT,
    DEFAULT_COOKING_TIME, DEFAULT_MEASUREMENT_UNIT, LENGTH_COLOR_07,
    LENGTH_MAIL_254, LENGTH_NAME_150, LENGTH_NAME_200,
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
        verbose_name=_('email address'),
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
        verbose_name=_('user name'),
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = CharField150(verbose_name=_('first name'))
    last_name = CharField150(verbose_name=_('last name'))
    password = CharField150(verbose_name=_('password'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscribe',
        through_fields=('follower', 'author'),
        verbose_name=_('subscriptions')
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email


class Subscribe(models.Model):
    """Подписки."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=_('author')
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('follower')
    )

    class Meta:
        constraints = [
            CHECK_SELF_SUBSCRIBE,
            CHECK_UNIQUE_SUBSCRIBE
        ]
        verbose_name = _('subscribe')
        verbose_name_plural = _('Subscribes')

    def __str__(self) -> str:
        return self.follower.email


class NameList(models.Model):
    """Абстрактный список наименований."""
    name = CharField200(verbose_name=_('item name'))

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Tag(NameList):
    """Тэги."""
    slug = models.SlugField(
        verbose_name=_('slug'), max_length=LENGTH_NAME_200, unique=True
    )
    color = models.CharField(
        verbose_name=_('color'), max_length=LENGTH_COLOR_07, validators=[color_validator]
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('Tags')


class MeasurementUnit(NameList):
    """Единицы измерения."""

    class Meta:
        verbose_name = _('measurement unit')
        verbose_name_plural = _('Measurement units')


class Ingridient(NameList):
    """Ингридиенты."""

    class Meta:
        verbose_name = _('ingridient')
        verbose_name_plural = _('Ingridients')


class Recipe(NameList):
    """Рецепты."""
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name=_('author'))
    tags = models.ManyToManyField(to=Tag, verbose_name=_('tags'))
    ingridients = models.ManyToManyField(
        to=Ingridient, through='RecipeIngridient', verbose_name=_('ingridients')
    )
    text = models.TextField(verbose_name=_('text'))
    cooking_time = models.SmallIntegerField(
        default=DEFAULT_COOKING_TIME,
        validators=[cooking_time_validator],
        verbose_name=_('cooking time')
    )
    image = models.ImageField(
        upload_to='recipes/images/', verbose_name=_('image')
    )

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('Recipes')


class RecipeIngridient(models.Model):
    """Ингридиенты в рецептах."""
    ingridient = models.ForeignKey(
        to=Ingridient,
        on_delete=models.CASCADE,
        related_name='ingridients',
        verbose_name=_('ingridient')
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('recipe')
    )
    amount = models.SmallIntegerField(
        verbose_name=_('amount'), default=DEFAULT_AMOUNT, validators=[amount_validator]
    )
    measurement_unit = models.ForeignKey(
        to=MeasurementUnit,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_MEASUREMENT_UNIT,
        verbose_name=_('measurement unit')
    )

    class Meta:
        constraints = [CHECK_UNUQUE_INGRIDIENT]
        verbose_name = _('ingridient in recipe')
        verbose_name_plural = _('Ingridients in recipe')

    def __str__(self) -> str:
        return f'[self.ingridient.name] [self.amount] [self.measurement_unit.name]'


class UserRecipe(models.Model):
    """Абстрактный список рецептов пользователя."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.recipe.name


class ShoppingCart(UserRecipe):
    """Корзина покупок."""

    class Meta:
        constraints = [
            CHECK_UNIQUE_SHOPPING
        ]
        verbose_name = _('recipe in shopping cart')
        verbose_name_plural = _('Recipes in shopping cart')


class FavoriteList(UserRecipe):
    """Любимые рецепты."""

    class Meta:
        constraints = [
            CHECK_UNIQUE_FAVORITE
        ]
        verbose_name = _('favorite recipe')
        verbose_name_plural = _('Favorite recipes')
