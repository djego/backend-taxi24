from django.db.models.expressions import RawSQL
from rest_framework import filters

class DistanceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        distance = request.GET.get('distance')
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
        if lat and lon and distance:
            return queryset\
                .annotate(distance=RawSQL(sql, (lat, lat, lon, lon)))\
                .filter(distance__lte=float(distance))\
                .order_by('distance')
        elif lat and lon:
            return queryset\
                .annotate(distance=RawSQL(sql, (lat, lat, lon, lon)))\
                .order_by('distance')
        return queryset