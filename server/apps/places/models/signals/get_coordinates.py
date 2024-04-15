from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.places.models.restaurant import Restaurant
from yandex_geocoder import Client
from config.settings.settings import YANDEX_API


@receiver(post_save, sender=Restaurant)
def get_coordinates(sender, instance, **kwargs):
    """
    Gets coordinates using Yandex Geocoder API and adds to restaurant's fields
    """
    if instance.latitude is None:
        client = Client(YANDEX_API)
        coordinates = client.coordinates(instance.address)
        instance.latitude = coordinates[1]
        instance.longitude = coordinates[0]
        instance.save()
