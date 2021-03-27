from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.filters import DistanceFilterBackend
from core.models import Driver, Passenger, Trip
from core.serializers import (DriverSerializer, PassengerSerializer,
    TripSerializer)

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = (DistanceFilterBackend, DjangoFilterBackend)
    filterset_fields = ('status',)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().select_related('passenger', 'driver')
    serializer_class = TripSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)

    @action(detail=True, methods=['put'], permission_classes=[])
    def ending(self, request, pk=None):
        trip = self.get_object()
        trip.status = Trip.END
        trip.save()
        return Response(TripSerializer(trip).data)
