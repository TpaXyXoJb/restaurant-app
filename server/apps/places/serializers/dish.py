from rest_framework import serializers
from apps.places.models.dish import Dish


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish model
    """
    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'photo',
            'total_calories',
            'ingredients',
            'restaurants'
        )
        read_only_fields = (
            'total_calories',
        )
