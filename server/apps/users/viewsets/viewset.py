from rest_framework import mixins
from rest_framework import viewsets

from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """

    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
