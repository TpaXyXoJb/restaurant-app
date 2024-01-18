from rest_framework import viewsets
from apps.places.models.dish import Dish
from apps.places.serializers.dish import DishSerializer
from apps.main.permissions.permissions import IsPlaceOwnerOrReadOnly


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsPlaceOwnerOrReadOnly]
