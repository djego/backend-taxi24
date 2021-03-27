from math import ceil
from uuid import uuid4
from django.db import models
from core import services

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Driver(BaseModel):
    AVAILABLE = 'A'
    UNAVAILABLE = 'U'
    STATUS = (
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
    )
    dni = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()
    status = models.CharField(max_length=2, choices=STATUS, default=AVAILABLE,
        blank=True)

    def __str__(self):
        return f"{self.name}({self.dni})"

class Passenger(BaseModel):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name

class Trip(BaseModel):
    ACTIVE = 'A'
    END = 'E'
    STATUS = (
        (ACTIVE, 'Active'),
        (END, 'End'),
    )
    source_lat = models.FloatField(null=True, blank=True)
    source_lon = models.FloatField(null=True, blank=True)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_lon = models.FloatField(null=True, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    distance = models.FloatField(default=0.0, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default=ACTIVE,
        blank=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE,
        related_name="trips")
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE,
        related_name="trips")

    def save(self, *args, **kwargs):
        if self.source_lat and self.source_lon and self.destination_lat \
                and self.destination_lon:
            self.distance = services.calculate_distance_haversine(
                self.source_lat,
                self.source_lon,
                self.destination_lat,
                self.destination_lon)
            self.cost = ceil(self.distance)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.driver} [{self.passenger}]"

class Bill(BaseModel):
    number = models.IntegerField(editable=False)
    driver = models.CharField(max_length=255, blank=True, null=True)
    passenger = models.CharField(max_length=255, blank=True, null=True)
    cost = models.FloatField(default=0.0, blank=True, null=True)
    distance = models.IntegerField(default=0, blank=True, null=True)
    trip = models.OneToOneField('Trip', on_delete=models.CASCADE,
        related_name="bill")
    
    def save(self, *args, **kwargs):
        self.driver = self.trip.driver.name
        self.passenger = self.trip.passenger.name
        self.cost = self.trip.cost
        self.distance = self.trip.distance
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Factura: {self.number}"
