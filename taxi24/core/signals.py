from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Bill, Trip, Driver

@receiver(post_save, sender=Trip)
def create_trip(sender, instance, created, **kwargs):
    if created:
        Driver.objects.filter(id=instance.driver_id)\
            .update(status=Driver.UNAVAILABLE)

@receiver(post_save, sender=Trip)
def ending_trip(sender, instance, **kwargs):
    if instance.status == Trip.END:
        Driver.objects.filter(id=instance.driver_id)\
            .update(status=Driver.AVAILABLE)
        params = {
            "number": Bill.objects.latest('created').number + 1,
            "trip": instance,
        }
        Bill.objects.create(**params)