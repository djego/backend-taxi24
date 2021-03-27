from uuid import uuid4
from django.db import models

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
    CANCEL = 'C'
    WAIT = 'W'
    STATUS = (
        (ACTIVE, 'Active'),
        (END, 'End'),
        (CANCEL, 'Cancel'),
        (WAIT, 'Wait'),
    )
    source = models.JSONField()
    destination = models.JSONField(null=True, blank=True)
    cost = models.FloatField(default=0.0, blank=True)
    distance = models.IntegerField(default=0, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default=WAIT,
        blank=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE,
        related_name="trips")
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE,
        related_name="trips")

    def __str__(self):
        return f"{self.driver} [{self.passenger}]"

class Bill(BaseModel):
    number = models.CharField(max_length=50)
    driver = models.CharField(max_length=255)
    passenger = models.CharField(max_length=255)
    cost = models.FloatField(default=0.0, blank=True)
    distance = models.IntegerField(default=0, blank=True)
    trip = models.OneToOneField('Trip', on_delete=models.CASCADE,
        related_name="bill")
    
    def __str__(self):
        return self.number
