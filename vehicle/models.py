from django.db import models

from config import settings


class Car(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(default=1000, verbose_name='Цена')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'машина'
        verbose_name_plural = 'машины'


class Moto(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'мотоцикл'
        verbose_name_plural = 'мотоциклы'


class Mileage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='mileage')
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, null=True, blank=True, related_name='mileage')

    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    year = models.PositiveSmallIntegerField(verbose_name='Год регистрации')

    def __str__(self):
        return f'{self.moto if self.moto else self.car} - {self.year}: {self.mileage}'

    class Meta:
        verbose_name = 'пробег'
        verbose_name_plural = 'пробег'
        ordering = ('-year',)


