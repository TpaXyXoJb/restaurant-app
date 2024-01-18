from django.db.models.signals import m2m_changed
from django.db.models import Sum
from django.dispatch import receiver
from apps.places.models.dish import Dish


@receiver(m2m_changed, sender=Dish.ingredients.through)
def get_total_calories(sender, instance, **kwargs):
    dish = Dish.objects.filter(id=instance.id)
    summ = dish.aggregate(Sum('ingredients__product_calorie'))
    value = summ.get('ingredients__product_calorie__sum') or 0
    instance.total_calories = value
    instance.save()
