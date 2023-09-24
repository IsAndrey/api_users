from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action

from .pagination import UsersPagination


class UserViewSet(DjoserViewSet):
    """
    Переопределяем вьюсет пользователей для добавления подписок
    и пагинации.
    """
    pagination_class = UsersPagination

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        ...

    @action(['post', 'delete'], detail=False)
    def subscribe(self, request, *args, **kwargs):
        ...
