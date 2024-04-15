from django.db.models.signals import post_save
from django.db.models import Avg
from django.dispatch import receiver
from apps.places.models.restaurant import Restaurant
from apps.places.models.dish import Dish


@receiver(post_save, sender=Dish)
def add_avg_price(sender, instance, **kwargs):
    """
    Adds average price to dish
    """
    restaurant = Restaurant.objects.get(pk=instance.restaurants_id)
    price = restaurant.dish_set.aggregate(Avg('price'))
    value = price.get('price__avg')
    Restaurant.objects.filter(pk=instance.restaurants_id).update(avg_cost=value)
