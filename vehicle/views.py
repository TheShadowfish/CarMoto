from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from vehicle.models import Car, Moto, Mileage
from vehicle.paginators import VehiclePaginator
from vehicle.permissions import IsOwnerOrStaff
from vehicle.serializers import CarSerializer, MotoSerializer, MileageSerializer, MotoMileageSerializer, \
    MotoCreateSerializer
from django_filters import rest_framework as filters

from vehicle.tasks import check_mileage


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()

class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    permission_classes = [IsOwnerOrStaff]



class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MileageCreateAPIView(generics.CreateAPIView):
    serializer_class = MileageSerializer
    def perform_create(self, serializer):
        new_mileage = serializer.save()
        if new_mileage.car:
            #check_mileage
            check_mileage.delay(new_mileage.car_id, 'Car')
        else:
            check_mileage.delay(new_mileage.moto_id, 'Moto')


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


