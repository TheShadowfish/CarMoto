from django.shortcuts import render
from rest_framework import viewsets, generics

from vehicle.models import Car, Moto, Mileage
from vehicle.serializers import CarSerializer, MotoSerializer, MileageSerializer, MotoMileageSerializer, \
    MotoCreateSerializer


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer

class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()



class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MileageCreateAPIView(generics.CreateAPIView):
    serializer_class = MileageSerializer


class MotoMileageListAPIView(generics.ListAPIView):
    queryset = Mileage.objects.filter(moto__isnull = False)
    serializer_class = MotoMileageSerializer
