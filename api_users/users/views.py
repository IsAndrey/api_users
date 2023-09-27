from djoser.views import UserViewSet as DjoserViewSet
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


from .pagination import UsersPagination
from .serializers import SubcribeSerializer
from .models import User, Subscribe


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
            author = get_object_or_404(User, id=kwargs.get('id', 0))
            data = {
                'author': author.id,
                'follower': request.user.id,
                'recipes_limit': request.query_params.get('recipes_limit', 1)
            }
            serializer = SubcribeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = self.get_serializer(instance=author)
            return Response(author_serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            # subscribe = get_object_or_404(Subscribe, author=kwargs.get('id', 0), follower=request.user.id)
            list = get_list_or_404(Subscribe, author=kwargs.get('id', 0), follower=request.user.id)
            for subscribe in list:
                subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
