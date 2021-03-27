from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from core.models import Driver, Passenger, Trip

class DriverSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'dni', 'name', 'manufacturer', 'model', 'plate', 'lat',
            'lon', 'status')

class PassengerSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'name', 'lat', 'lon')

class TripSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'source', 'destination', 'cost', 'distance', 'status',
            'driver', 'passenger')