from django.db import models
from django.db.models import BooleanField

from reservation import consts

class Tables(models.Model):
    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    name = models.CharField(max_length=255, verbose_name='Наименование')
    seats = models.PositiveIntegerField(editable=True, null=False, blank=False, default=0,
                                        verbose_name='Количество мест')
    location = models.CharField(max_length=255, editable=True, null=False, blank=False,
                                choices=consts.LOCATION_CHOICES, verbose_name='Местонахождение')
    busyness = models.BooleanField(default=False, verbose_name='Занятость')

    def __str__(self):
        return self.name


class Reservation(models.Model):
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    customer_name = models.CharField(max_length=255, editable=True, null=False, blank=False, verbose_name='Имя заказчика')
    table_id = models.ForeignKey(Tables, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(editable=True, null=False, blank=False)
    active = BooleanField(default=True)