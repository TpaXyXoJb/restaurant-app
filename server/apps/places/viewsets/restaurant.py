from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from apps.places.models.restaurant import Restaurant
from apps.places.serializers.restaurant import RestaurantSerializer
from apps.main.permissions.permissions import IsOwnerOrReadOnly
from apps.places.filters.filters import DjangoFilterDescriptionInspector, RestaurantFilter


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector]
))
@method_decorator(name='list', decorator=cache_page(timeout=60 * 15))
@method_decorator(name='retrieve', decorator=cache_page(timeout=60 * 15))
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RestaurantFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
