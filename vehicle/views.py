from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from vehicle.models import Car, Moto, Mileage
from vehicle.serializers import CarSerializer, MotoSerializer, MileageSerializer, MotoMileageSerializer, \
    MotoCreateSerializer
from django_filters import rest_framework as filters

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

class MileageFilter(filters.FilterSet):
    # filter_queryset = Mileage.objects.all()
    car = filters.ModelChoiceFilter(queryset=Car.objects.all(), null_label='null')
    moto = filters.ModelChoiceFilter(queryset=Moto.objects.all(), null_label='null')

class Meta:
    model = Mileage
    fields = ['car', 'moto']

class MileageListAPIView(generics.ListAPIView):
    serializer_class = MileageSerializer
    queryset = Mileage.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = MileageFilter
    # filterset_fields = ('car', 'moto')
    filterset_class = MileageFilter
    ordering_fields = ('year',)


