from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters
from apps.places.models.dish import Dish
from apps.places.serializers.dish import DishSerializer
from apps.main.permissions.permissions import IsPlaceOwnerOrReadOnly
from apps.places.filters.filters import DjangoFilterDescriptionInspector, DishFilter


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector]
))
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsPlaceOwnerOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DishFilter
