from django.contrib import admin

from .models import (
    Tag, Ingridient, Recipe, Subscribe, FavoriteList, ShoppingCart, User, MeasurementUnit, RecipeIngridient
)


class FavoriteListInLine(admin.StackedInline):
    model = FavoriteList
    extra = 0


class ShoppingCartInLine(admin.StackedInline):
    model = ShoppingCart
    extra = 0


class SubscribeInLine(admin.StackedInline):
    model = Subscribe
    extra = 0
    fk_name = 'author'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (FavoriteListInLine, ShoppingCartInLine, SubscribeInLine)


class RecipeIngridientInLine(admin.StackedInline):
    model = RecipeIngridient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngridientInLine,)


admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(MeasurementUnit)
