from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.conf import settings
from rest_framework import serializers
from rest_framework.validators import qs_exists, qs_filter, UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from .models import User, Subscribe


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)
    
    def get_is_subscribed(self, author):
        follower = self.context['request'].user
        return qs_exists(qs_filter(Subscribe.objects.all(), author=author, follower=follower))


class SubcribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('author', 'follower')
            ),
        ]

    def validate(self, attrs):
        author = attrs.get('author', None)
        follower = attrs.get('follower', None)
        if author is None or follower is None or author == follower:
            raise ValidationError(_('Fields follower and author should not be None or equal'), code='unique')
        return super().validate(attrs)
