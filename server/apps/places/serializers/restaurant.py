from rest_framework import serializers

from apps.places.models.restaurant import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'owner',
            'opening_time',
            'closing_time',
            'photo',
            'address',
            'avg_cost',
            'latitude',
            'longitude',
        )
        read_only_fields = (
            'owner',
        )
