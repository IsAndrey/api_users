from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action


class UserViewSet(DjoserViewSet):
    """Переопределяем вьюсет пользователей для добавления подписок."""

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        ...

    @action(['post', 'delete'], detail=False)
    def subscribe(self, request, *args, **kwargs):
        ...
