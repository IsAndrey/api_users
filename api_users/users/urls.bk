from django.urls import include, path
from .views import UserViewSet


urlpatterns = [
    path('users/', UserViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('users/<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/me/', UserViewSet.as_view({'get': 'me'})),
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', UserViewSet.as_view({'get': 'subscriptions'})),
    path('users/<int:id>/subscribe/', UserViewSet.as_view(
        {
            'post': 'subscribe',
            'delete': 'subscribe'
        }
    ))
]
