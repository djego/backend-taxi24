"""
Models for taxi24 api.
"""
from math import ceil
from uuid import uuid4
from django.db import models
from django.db.models.expressions import RawSQL
from core import services

class BaseModel(models.Model):
    """
    BaseModel with basic fields.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DriverManager(models.Manager):
    """
    Manager for custom queries.
    """
    def filter_distance(self, lat, lon, distance):
        return self.order_by_distance(lat, lon)\
            .filter(distance__lte=float(distance))

    def order_by_distance(self, lat, lon):
        sql = """
        SELECT asin(
            sqrt(
                sin(radians(%s-lat)/2) * sin(radians(%s-lat)/2) +
                sin(radians(%s-lon)/2) * sin(radians(%s-lon)/2) *
                cos(radians(lat)) *
                cos(radians(lon))
            )
        ) * 2 * 6371 
        """
        return self.annotate(distance=RawSQL(sql, (lat, lat, lon, lon)))\
            .order_by('distance')

class Driver(BaseModel):
    """
    Driver Model for table core_driver.
    """
    AVAILABLE = 'A'
    UNAVAILABLE = 'U'
    STATUS = (
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
    )
    dni = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()
    status = models.CharField(max_length=2, choices=STATUS, default=AVAILABLE,
        blank=True)

    objects = DriverManager()

    def __str__(self):
        return f"{self.name}({self.dni})"

class Passenger(BaseModel):
    """
    Passenger Model for table core_passenger.
    """
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name

class Trip(BaseModel):
    """
    Trip model for table core_trip.
    """
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
        """
        Override save and set distance and cost.
        """
        if self.source_lat and self.source_lon and self.destination_lat \
                and self.destination_lon:
            self.distance = services.calculate_haversine_distance(
                self.source_lat,
                self.source_lon,
                self.destination_lat,
                self.destination_lon)
            self.cost = ceil(self.distance)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.driver} [{self.passenger}]"

class Bill(BaseModel):
    """
    Bill model for table core_bill.
    """
    number = models.IntegerField(editable=False)
    driver = models.CharField(max_length=255, blank=True, null=True)
    passenger = models.CharField(max_length=255, blank=True, null=True)
    cost = models.IntegerField(default=0, blank=True, null=True)
    distance = models.FloatField(default=0.0, blank=True, null=True)
    trip = models.OneToOneField('Trip', on_delete=models.CASCADE,
        related_name="bill")

    def save(self, *args, **kwargs):
        """
        Override save and set values from trip.
        """
        self.driver = self.trip.driver.name
        self.passenger = self.trip.passenger.name
        self.cost = self.trip.cost
        self.distance = self.trip.distance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura: {self.number}"
