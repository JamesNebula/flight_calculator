"""Tests for distance calculation functions."""
import pytest
from services.distance_calculator import (
    haversine_distance,
    calculate_initial_bearing,
    bearing_to_compass_direction
)

def test_haversine_lax_to_jfk():
    """
    Test LAX to JFK distance.
    Known distance: approximately 2,475 miles
    Source: aviation industry standard measurements
    """
    lax_coords = (33.9425, -118.4081)
    jfk_coords = (40.6413, -73.7781)
    
    distance = haversine_distance(lax_coords, jfk_coords, 'miles')
    
    # Allow 10 mile tolerance for calculation differences
    assert 2465 < distance < 2485, f"Expected ~2475 miles, got {distance}"

def test_haversine_same_point():
    """Distance between same point should be zero."""
    coords = (40.0, -75.0)
    distance = haversine_distance(coords, coords, 'miles')
    assert distance == 0.0

def test_bearing_north():
    """Bearing from equator to north pole should be 0 degrees."""
    equator = (0.0, 0.0)
    north_pole = (90.0, 0.0)
    bearing = calculate_initial_bearing(equator, north_pole)
    assert abs(bearing - 0.0) < 0.1

def test_bearing_east():
    """Bearing along equator eastward should be 90 degrees."""
    point1 = (0.0, 0.0)
    point2 = (0.0, 10.0)
    bearing = calculate_initial_bearing(point1, point2)
    assert abs(bearing - 90.0) < 0.1

def test_compass_directions():
    """Test compass direction conversion."""
    assert bearing_to_compass_direction(0.0) == "N"
    assert bearing_to_compass_direction(45.0) == "NE"
    assert bearing_to_compass_direction(90.0) == "E"
    assert bearing_to_compass_direction(180.0) == "S"
    assert bearing_to_compass_direction(270.0) == "W"
    assert bearing_to_compass_direction(359.0) == "N"  # Wraps around