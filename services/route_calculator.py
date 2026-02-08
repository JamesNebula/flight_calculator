"""Business logic for flight route calculations."""
from services.distance_calculator import (
    haversine_distance,
    calculate_initial_bearing,
    bearing_to_compass_direction
)
from models.airport import FlightRoute

# Assumed average commercial jet speed (for time estimation)
AVERAGE_CRUISE_SPEED_MPH = 500.0

def calculate_flight_route(origin, destination):
    """
    Calculate complete flight route information between two airports.
    
    Arguments:
        origin: Airport object (departure)
        destination: Airport object (arrival)
    
    Returns:
        FlightRoute object with all calculated metrics, or None if invalid
    """
    # Validation
    if origin.code == destination.code:
        print(f"Origin and destination cannot be the same airport ({origin.code})")
        return None
    
    # Get coordinates
    coords_origin = origin.get_coordinates()
    coords_dest = destination.get_coordinates()
    
    # Calculate distances in all units
    distance_miles = haversine_distance(coords_origin, coords_dest, 'miles')
    distance_km = haversine_distance(coords_origin, coords_dest, 'km')
    distance_nm = haversine_distance(coords_origin, coords_dest, 'nautical_miles')
    
    # Calculate navigation data
    bearing = calculate_initial_bearing(coords_origin, coords_dest)
    compass_direction = bearing_to_compass_direction(bearing)
    
    # Estimate flight time
    estimated_hours = distance_miles / AVERAGE_CRUISE_SPEED_MPH
    
    # Create and return route object
    return FlightRoute(
        origin=origin,
        destination=destination,  
        distance_miles=distance_miles,
        distance_km=distance_km,
        distance_nautical_miles=distance_nm,
        bearing_degrees=bearing,
        compass_direction=compass_direction,
        estimated_flight_hours=estimated_hours
    )


def validate_airport_codes(origin_code, destination_code, airports):
    """
    Validate airport codes and return corresponding Airport objects.
    
    Returns:
        Tuple of (origin_airport, destination_airport) or (None, None) if invalid
    """
    origin_code = origin_code.strip().upper()
    destination_code = destination_code.strip().upper()
    
    if origin_code not in airports:
        print(f"Origin airport '{origin_code}' not found in database")
        return None, None
    
    if destination_code not in airports:
        print(f"Destination airport '{destination_code}' not found in database")
        return None, None
    
    if origin_code == destination_code:
        print(f"Origin and destination cannot be the same airport ({origin_code})")
        return None, None
    
    return airports[origin_code], airports[destination_code]