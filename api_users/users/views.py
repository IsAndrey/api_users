from djoser.views import UserViewSet as DjoserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .pagination import UsersPagination
from .models import User
from .serializers import UserSerializer


class UserViewSet(DjoserViewSet):
    """
    Переопределяем вьюсет пользователей для добавления подписок
    и пагинации.
    """
    pagination_class = UsersPagination

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)

    @action(['post', 'delete'], detail=False)
    def subscribe(self, request, *args, **kwargs):
        if request.method == "POST":
            author = get_object_or_404(User, id=kwargs.get('id'))
            follower = request.user
            recipes_limit = request.POST.get('recipes_limit')
