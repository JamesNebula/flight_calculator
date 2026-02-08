"""Geodesic distance and bearing calculations using Haversine formula."""
import math
from config.constants import (
    EARTH_RADIUS_KM,
    EARTH_RADIUS_MILES,
    EARTH_RADIUS_NAUTICAL_MILES,
    COMPASS_DIRECTIONS,
    COMPASS_SEGMENT_SIZE
)

def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    return degrees * math.pi / 180.0


def haversine_distance(coord1, coord2, unit='miles'):
    """
    Calculate great-circle distance between two coordinates using Haversine formula.
    
    Arguments:
        coord1: (latitude, longitude) of first point in decimal degrees
        coord2: (latitude, longitude) of second point in decimal degrees
        unit: 'miles', 'km', or 'nautical_miles'
    
    Returns:
        Distance in specified units, rounded to 2 decimal places
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert to radians
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    lon2_rad = degrees_to_radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Select radius based on unit
    if unit == 'km':
        radius = EARTH_RADIUS_KM
    elif unit == 'nautical_miles':
        radius = EARTH_RADIUS_NAUTICAL_MILES
    else:
        radius = EARTH_RADIUS_MILES
    
    distance = radius * c
    return round(distance, 2)


def calculate_initial_bearing(coord1, coord2):
    """
    Calculate initial compass bearing from point 1 to point 2.
    
    Returns:
        Bearing in degrees (0-360), rounded to 1 decimal place
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    dlon_rad = degrees_to_radians(lon2 - lon1)
    
    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad))
    
    bearing_rad = math.atan2(y, x)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360
    
    return round(bearing_deg, 1)


def bearing_to_compass_direction(bearing):
    """
    Convert numeric bearing to human-readable compass direction.
    
    Arguments:
        bearing: Degrees (0-360)
    
    Returns:
        Compass direction (e.g., "NNE", "SW")
    """
    index = round(bearing / COMPASS_SEGMENT_SIZE) % 16
    return COMPASS_DIRECTIONS[index]