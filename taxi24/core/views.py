from rest_framework import viewsets
from core.models import Driver, Passenger, Trip
from core.serializers import (DriverSerializer, PassengerSerializer,
    TripSerializer)

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filterset_fields = ('status',)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().select_related('passenger', 'driver')
    serializer_class = TripSerializer
    filterset_fields = ('status',)
