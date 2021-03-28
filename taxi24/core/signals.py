"""
Signals for taxi24 models.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Bill, Trip, Driver, Passenger

@receiver(post_save, sender=Trip)
def create_trip(sender, instance, created, **kwargs):
    """
    Update status for driver when trip is created.
    """
    if created:
        # Change status for driver.
        Driver.objects.filter(id=instance.driver_id)\
            .update(status=Driver.UNAVAILABLE)

@receiver(post_save, sender=Trip)
def ending_trip(sender, instance, **kwargs):
    """
    Actions when trip was ended.
    """
    if instance.status == Trip.END:
        # Change status for driver.
        Driver.objects.filter(id=instance.driver_id)\
            .update(status=Driver.AVAILABLE)
        # Create bill.
        try:
            number = Bill.objects.latest('created').number + 1
        except Exception as e:
            number = 1
        params = {
            "number": number,
            "trip": instance,
        }
        Bill.objects.create(**params)
        # Change location for driver and passenger.
        if instance.destination_lat and instance.destination_lon:
            Driver.objects.filter(id=instance.driver_id).update(
                lat=instance.destination_lat,lon=instance.destination_lon)
            Passenger.objects.filter(id=instance.passenger_id).update(
                lat=instance.destination_lat,lon=instance.destination_lon)
