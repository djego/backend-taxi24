from django.db.models.expressions import RawSQL
from rest_framework import filters
from core.models import Driver

class DriverDistanceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        distance = request.GET.get('distance')
        if lat and lon and distance:
            return Driver.objects.filter_distance(lat, lon, distance)
        elif lat and lon:
            return Driver.objects.order_by_distance(lat, lon)
        return queryset