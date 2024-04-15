from rest_framework import serializers
from apps.places.models.ingredient import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredient model
    """
    class Meta:
        model = Ingredient
        fields = "__all__"
