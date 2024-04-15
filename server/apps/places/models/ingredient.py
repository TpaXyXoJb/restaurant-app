from django.db import models


class Ingredient(models.Model):
    """
    Ingredient model
    """
    name = models.CharField(max_length=128, verbose_name="Название продукта")
    product_calorie = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Калорийность продукта")

    class Meta:
        verbose_name = "Название продукта"
        verbose_name_plural = "Нзвание продуктов"

    def __str__(self):
        return self.name
