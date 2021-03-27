from rest_framework import serializers
from core.models import Driver, Passenger, Trip

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'dni', 'name', 'manufacturer', 'model', 'plate', 'lat',
            'lon', 'status')

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'name', 'lat', 'lon')

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'source', 'destination', 'cost', 'distance', 'status',
            'driver', 'passenger')