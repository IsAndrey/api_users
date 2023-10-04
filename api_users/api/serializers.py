from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import (
    UniqueTogetherValidator, qs_exists, qs_filter
)

from recipes.models import (
    FavoriteList, Ingridient, Recipe, ShoppingCart, Subscribe, Tag, User
)
from recipes.validators import DEFAULT_LIST_LIMIT


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)
    
    def get_is_subscribed(self, author):
        follower = self.context['request'].user
        return qs_exists(qs_filter(
            Subscribe.objects.all(), author=author, follower=follower
        ))


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Для чтения рецептов блюд."""

    def to_representation(self, instance):
        return super().to_representation(instance)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipesSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = SimpleRecipeSerializer(read_only=True, many=True)
    recipes_limit = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
            'recipes_count',
            'recipes',
            'recipes_limit'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_recipes_count(self, author):
        qs = qs_filter(Recipe, author=author)
        if qs_exists(qs):
            return qs.count()
        else:
            return 0
     
    def get_recipes_limit(self, author):
        return self.context['request'].query_params.get('recipes_limit', DEFAULT_LIST_LIMIT)
        

class SubcribeSerializer(serializers.ModelSerializer):
    """Для записи подписок пользователя."""

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('author', 'follower')
            ),
        ]

    def validate(self, attrs):
        author = attrs.get('author', None)
        follower = attrs.get('follower', None)
        if not isinstance(author, type(follower)):
            error_message = _(
                'Fields follower and author must be of the same type.'
            )
            raise ValidationError(error_message, code='unique')
        elif author == follower:
            error_message = _(
                'Fields follower and author should not be equal.'
            )
            raise ValidationError(error_message, code='unique')
        return super().validate(attrs)


class RecipeSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def check_query_set(self, recipe, query_set):
        user = self.context['request'].user
        return qs_exists(qs_filter(
            query_set, user=user, recipe=recipe
        ))

    def get_is_favorite(self, recipe):
        return self.check_query_set(
            recipe=recipe,
            query_set=FavoriteList.objects.all()
        )

    def get_is_in_shopping_cart(self, recipe):
        return self.check_query_set(
            recipe=recipe,
            query_set=ShoppingCart.objects.all()
        )


class TagSerializer(serializers.ModelSerializer):
    """Для чтения тэгов-категорий рецептов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngridientSerializer(serializers.ModelSerializer):
    """Для чтения ингридиентов."""

    class Meta:
        model = Ingridient
        fields = '__all__'


class FavoriteListSerializer(serializers.ModelSerializer):
    """ЗДля записи подписок и покупок."""

    class Meta:
        model = FavoriteList
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Для записи в корзину покупок."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'
