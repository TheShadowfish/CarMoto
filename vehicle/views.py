from django.shortcuts import render
from rest_framework import viewsets, generics

from vehicle.models import Car
from vehicle.serializers import CarSerializer, MotoSerializer


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoSerializer


