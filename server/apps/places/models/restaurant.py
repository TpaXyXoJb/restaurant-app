from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название заведения")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец заведения",
                              related_name='restaurants')
    opening_time = models.TimeField(verbose_name="Время открытия")
    closing_time = models.TimeField(verbose_name="Время закрытия")
    photo = models.ImageField(null=True, verbose_name="Фото заведения")
    address = models.CharField(max_length=256, verbose_name="Адрес заведения")
    avg_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                                   verbose_name='Средняя стоимость')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Долгота")

    class Meta:
        verbose_name = "Название заведения"
        verbose_name_plural = "Название заведений"

    def __str__(self):
        return self.name
