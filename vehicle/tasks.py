from celery import shared_task
from django.utils.datetime_safe import datetime

from vehicle.models import Car, Moto

@shared_task
def check_mileage(pk, model):
    if model == 'Car':
        instance = Car.objects.filter(pk=pk).first()
    else:
        instance = Moto.objects.filter(pk=pk).first()


    if instance:
        prev_mileage = -1
        for m in instance.mileage.all():
            if prev_mileage == -1:
                prev_mileage = m.mileage
            else:
                if prev_mileage < m.mileage:
                    print("Неверный пробег")
                    break


@shared_task
def my_task():
    time = datetime.now()

    print(f"time now: {time}")


def check_filter():
    filter_price = {"price__lte": 500}
    if Car.objects.filter(**filter_price).exist():
        print("Отчет по фильтру")