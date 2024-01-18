from rest_framework import viewsets
from apps.places.models.restaurant import Restaurant
from apps.places.serializers.restaurant import RestaurantSerializer
from apps.main.permissions.permissions import IsOwnerOrReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)