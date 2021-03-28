"""
Config admin site.
"""
from django.contrib import admin
from core.models import Driver, Passenger, Trip, Bill

admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Trip)
admin.site.register(Bill)
