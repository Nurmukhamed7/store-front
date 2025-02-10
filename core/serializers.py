from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):

    # Inherit all from (BaseUserCreateSerializer.Meta)
    class Meta(BaseUserCreateSerializer.Meta):

        # Overriding fields
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

# this class for customize /auth/users/me/
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
