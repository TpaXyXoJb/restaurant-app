from rest_framework.serializers import ModelSerializer, SerializerMethodField

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(ModelSerializer):
    """
    Serializer for user model
    """
    token = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'token'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.get_or_create(user=user)
        return user

    def get_token(self, user):
        token = user.auth_token
        return token.key
