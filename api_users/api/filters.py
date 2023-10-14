from django_filters import rest_framework as filters
from rest_framework.validators import qs_filter

from recipes.models import FavoriteList, Recipe, ShoppingCart


class RecipesFilters(filters.FilterSet):
    """Фильтр для модели Recipe."""
    author = filters.NumberFilter(field_name='author')
    tags = filters.CharFilter(field_name='tag__slug')
    is_favorite = filters.CharFilter(method='get_is_favorite')
    is_in_shopping_cart = filters.CharFilter(method='get_is_in_shopping_cart')

    def get_filtered_recipes(self, queryset, checked_queryset, value):
        user = getattr(self.request, 'user', None)
        if user is None or value not in ('0', '1'):
            return queryset
        filtred_recipes = qs_filter(checked_queryset, user=user)
        if bool(int(value)):
            queryset.filter(
                id__in=[recipe.id for recipe in filtred_recipes]
            )
        else:
            queryset.exclude(
                id__in=[recipe.id for recipe in filtred_recipes]
            )
        return queryset

    def get_is_favorite(self, queryset, name, value):
        return self.get_filtred_recipes(
            queryset, FavoriteList.objects, value
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        return self.get_filtred_recipes(
            queryset, ShoppingCart.objects, value
        )

    class Meta:
        model = Recipe
        fields = ('is_favorite', 'is_in_shopping_cart', 'author', 'tags')
