"""
Filters Backend for querysets.
"""
from rest_framework import filters
from core.models import Driver

class DriverDistanceFilterBackend(filters.BaseFilterBackend):
    """
    FilterBackend for driver distance.
    """
    def filter_queryset(self, request, queryset, view):
        """
        Use custom query for driver distance.
        """
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        distance = request.GET.get('distance')
        new_qs = queryset
        if lat and lon and distance:
            new_qs = Driver.objects.filter_distance(lat, lon, distance)
        elif lat and lon:
            new_qs = Driver.objects.order_by_distance(lat, lon)
        return new_qs
