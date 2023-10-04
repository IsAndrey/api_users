from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    FavoriteList, Ingridient, Recipe, ShoppingCart, Subscribe, Tag, User
)
from recipes.validators import (
    DEFAULT_LIST_LIMIT, CHECK_UNIQUE_RECIPE, CHECK_UNIQUE_SUBSCRIBE
)
from .serializers import (
    FavoriteListSerializer, IngridientSerializer, RecipeSerializer, 
    ShoppingCartSerializer, SimpleRecipeSerializer, SubcribeSerializer,
    TagSerializer, UserRecipesSerializer
)
from .pagination import UsersPagination


class UserViewSet(DjoserViewSet):
    """
    Переопределяем вьюсет пользователей для добавления подписок
    и пагинации.
    """
    pagination_class = UsersPagination

    def get_queryset(self):
        if self.action == 'subscriptions':
            follower = self.request.user
            return follower.subscriptions.all()
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return UserRecipesSerializer
        return super().get_serializer_class()

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(['post', 'delete'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        if request.method == "POST":
            author = get_object_or_404(User, id=kwargs.get('id', 0))
            recipes_limit = request.query_params.get(
                'recipes_limit',
                DEFAULT_LIST_LIMIT
            )
            data = {
                'author': author.id,
                'follower': request.user.id
            }
            serializer = SubcribeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_recipes_serializer = UserRecipesSerializer(
                instance=author
            )
            return Response(
                user_recipes_serializer.data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == "DELETE":
            # Проверим ограничения модели Subscribe
            has_unique_constraint = (
                Subscribe.Meta.constraints and
                CHECK_UNIQUE_SUBSCRIBE in Subscribe.Meta.constraints
            )
            if has_unique_constraint:
                subscribe = get_object_or_404(
                    Subscribe,
                    author=kwargs.get('id', 0),
                    follower=request.user.id
                )
                subscribe.delete()
            else:
                list = get_list_or_404(
                    Subscribe,
                    author=kwargs.get('id', 0),
                    follower=request.user.id
                )
                for subscribe in list:
                    subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipe."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_action(self, request, **kwargs):
        instance_model = Recipe
        read_serializer_class = SimpleRecipeSerializer
        list_model = kwargs.get('list_model', None)
        write_serializer_class = kwargs.get('write_serializer_class', None)

        if list_model is None or write_serializer_class is None:
            Response(status=status.HTTP_418_IM_A_TEAPOT)

        if request.method == 'POST':
            instance = get_object_or_404(instance_model, id=kwargs.get('id',0))
            data = {
                'user': request.user.id,
                'recipe': instance.id
            }
            recipes_limit = request.query_params.get(
                'recipes_limit',
                DEFAULT_LIST_LIMIT
            )
            write_serializer = write_serializer_class(data=data)
            write_serializer.is_valid(raise_exception=True)
            write_serializer.save()
            read_serializer = read_serializer_class(
                instance=instance, recipes_limit=recipes_limit
            )
            Response(read_serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            has_unique_constraint = (
                list_model.Meta.constraints and
                CHECK_UNIQUE_RECIPE in list_model.Meta.constraints
            )
            if has_unique_constraint:
                unit = get_object_or_404(
                    list_model,
                    user=request.user.id,
                    recipe=kwargs.get('id', 0)
                )
                Response(status=status.HTTP_204_NO_CONTENT)
            else:
                list = get_list_or_404(
                    list_model,
                    user=request.user.id,
                    recipe=kwargs.get('id', 0)
                )
                for unit in list:
                    unit.delete()
                Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        self.perform_action(
            request=request,
            list_model=ShoppingCart,
            write_serializer_class=ShoppingCartSerializer
        )

    @action(['get'], detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ...
    
    @action(['post', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        self.perform_action(
            request=request,
            list_model=FavoriteList,
            write_serializer_class = FavoriteListSerializer
        )

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingridient."""
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
