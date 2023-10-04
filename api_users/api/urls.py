from django.urls import include, path
from rest_framework import routers

from .views import (
    IngridientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet    
)


recipes_router = routers.DefaultRouter()
recipes_router.register(r'recipes', RecipeViewSet)
recipes_router.register(r'tags', TagViewSet)
recipes_router.register(r'ingridients', IngridientViewSet)

urlpatterns = [
    path('', include(recipes_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', UserViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('users/<int:id>/', UserViewSet.as_view(
        {'get': 'retrieve'}
    )),
    path('users/me/', UserViewSet.as_view(
        {'get': 'me'}
    )),
    path('users/set_password/', UserViewSet.as_view(
        {'post': 'set_password'}
    )),
    path('users/subscriptions/', UserViewSet.as_view(
        {'get': 'subscriptions'}
    )),
    path('users/<int:id>/subscribe/', UserViewSet.as_view(
        {
            'post': 'subscribe',
            'delete': 'subscribe'
        }
    ))
]
