from django.contrib import admin

from .models import (
    Tag, Ingridient, Recipe, Subscribe, FavoriteList, ShoppingCart, User
)

class TagInLine(admin.StackedInline):
    model = Tag
    extra = 0


class IngridientInLine(admin.StackedInline):
    model = Ingridient
    extra = 0


class SubscribeInLine(admin.StackedInline):
    model = Subscribe
    extra = 0


class FavoriteListInLine(admin.StackedInline):
    model = FavoriteList
    extra = 0


class ShoppingCartInLine(admin.StackedInline):
    model = ShoppingCart
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (FavoriteListInLine, ShoppingCartInLine)


admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(Recipe)
