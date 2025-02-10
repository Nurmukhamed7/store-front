from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):

    # Inherit all from (BaseUserCreateSerializer.Meta)
    class Meta(BaseUserCreateSerializer.Meta):

        # Overriding fields
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']