from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key},
                        status=status.HTTP_201_CREATED,
                        headers=headers
                        )
