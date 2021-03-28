from math import sin, cos, sqrt, atan2, radians, ceil

def calculate_haversine_distance(source_lat, source_lon, destination_lat,
    destination_lon):
    
    R = 6373.0
    dlon = radians(destination_lon) - radians(source_lon)
    dlat = radians(destination_lat) - radians(source_lat)
    a = sin(dlat / 2)**2 \
        + cos(source_lat) * cos(destination_lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c