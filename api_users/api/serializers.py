import base64

from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
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
    """Для чтения пользователей."""
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
            Subscribe.objects, author=author, follower=follower
        ))


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Для чтения рецептов блюд."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipesSerializer(UserSerializer):
    """Для чтения пользователей с рецептами блюд."""
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
            'recipes_count',
            'recipes'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_recipes_count(self, author):
        qs = qs_filter(Recipe.objects, author=author)
        if qs_exists(qs):
            return qs.count()
        else:
            return 0
    
    def get_recipes(self, author):
        recipes_limit = int(self.context['request'].query_params.get(
            'recipes_limit', DEFAULT_LIST_LIMIT
        ))
        qs = qs_filter(Recipe.objects, author=author)[:recipes_limit]
        serializer = SimpleRecipeSerializer(qs, many=True)
        return serializer.data


class SubcribeSerializer(serializers.ModelSerializer):
    """Для записи подписок пользователя."""

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects,
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


class Base64ImageField(serializers.ImageField):
    """Поле для записи изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imagestr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imagestr), name='image.' + ext)

        return super().to_internal_value(data)


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


class WriteRecipeSerializer(serializers.ModelSerializer):
    """Для записи рецептов."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag = get_object_or_404(Tag, **tag)
            recipe.tags.create(tag=current_tag)
        for ingridient in ingridients:
            amount = ingridient.pop('amount')
            current_ingridient = get_object_or_404(Ingridient, **ingridient)
            recipe.ingridients.create(
                ingridient=current_ingridient, amount=amount
            )

        return recipe
    
    def update(self, recipe, validated_data):
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        list_of_tags = [get_object_or_404(Tag, **tag) for tag in tags]
        recipe.tags.set(list_of_tags)
        for ingridient in ingridients:
            amount = ingridient.pop('amount')
            current_ingridient = get_object_or_404(Ingridient, **ingridient)
            recipe.ingridients.create_or_update(
                ingridient=current_ingridient, amount=amount
            )
        # Удаляем лишние ингридиенты из рецепта.
        deleted_ingridients = recipe.ingridients.exclude(
            id__in=[ingridient.get('id',0) for ingridient in ingridients]
        )
        if qs_exists(deleted_ingridients):
            for deleted_ingridient in deleted_ingridients:
                deleted_ingridient.delete()

        return recipe


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Для чтения рецептов."""
    tags = TagSerializer(read_only=True, many=True)
    ingridients = IngridientSerializer(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

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
            query_set=FavoriteList.objects
        )

    def get_is_in_shopping_cart(self, recipe):
        return self.check_query_set(
            recipe=recipe,
            query_set=ShoppingCart.objects
        )

    def get_image(self, recipe):
        return recipe.image.url


class FavoriteListSerializer(serializers.ModelSerializer):
    """Для записи в избранное."""

    class Meta:
        model = FavoriteList
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Для записи в корзину покупок."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'
