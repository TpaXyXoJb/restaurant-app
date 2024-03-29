from rest_framework import viewsets
from rest_framework import mixins
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.places.models.ingredient import Ingredient
from apps.places.serializers.ingredient import IngredientSerializer
from apps.places.filters.filters import DjangoFilterDescriptionInspector, IngredientFilter


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector]
))
class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IngredientFilter
