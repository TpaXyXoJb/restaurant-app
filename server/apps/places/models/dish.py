from django.db import models
from .ingredient import Ingredient
from .restaurant import Restaurant


class Dish(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название блюда")
    photo = models.ImageField(null=True, verbose_name="Фото блюда")
    total_calories = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Общая калорийность")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость блюда")
    ingredients = models.ManyToManyField(Ingredient, verbose_name="Ингредиенты")
    restaurants = models.ForeignKey(Restaurant, verbose_name="Связанные заведения", null=True, blank=True,
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Название блюда"
        verbose_name_plural = "Нзвание блюд"

    def __str__(self):
        return self.name
