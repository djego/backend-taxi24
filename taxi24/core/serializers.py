"""
Serializers for taxi24 models.
Use DynamicFieldsMixin for filter fields.
"""
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from core.models import Driver, Passenger, Trip

class DriverSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for Driver model.
    """
    class Meta:
        model = Driver
        fields = ('id', 'dni', 'name', 'manufacturer', 'model', 'plate', 'lat',
            'lon', 'status')

class PassengerSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for Passenger model.
    """
    class Meta:
        model = Passenger
        fields = ('id', 'name', 'lat', 'lon')

class TripSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for Trip model.
    """
    class Meta:
        model = Trip
        fields = ('id', 'source_lat', 'source_lon', 'destination_lat',
            'destination_lon', 'cost', 'distance', 'status', 'driver',
            'passenger')
