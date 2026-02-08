"""Tests for flight route calculation."""
import pytest
from models.airport import Airport
from services.route_calculator import calculate_flight_route

def test_route_calculation():
    """Test basic route calculation between two airports."""
    lax = Airport("LAX", "Los Angeles International", "Los Angeles", "USA", 33.9425, -118.4081)
    jfk = Airport("JFK", "John F. Kennedy International", "New York", "USA", 40.6413, -73.7781)
    
    route = calculate_flight_route(lax, jfk)
    
    assert route is not None
    assert route.origin.code == "LAX"
    assert route.destination.code == "JFK"  # CRITICAL: Verify destination is correct
    
    # Check distance is reasonable
    assert 2400 < route.distance_miles < 2600
    
    # Check bearing is reasonable (east-northeast from LAX to JFK)
    assert 60 < route.bearing_degrees < 80

def test_same_airport_rejected():
    """Route calculation should reject same origin/destination."""
    lax = Airport("LAX", "Los Angeles International", "Los Angeles", "USA", 33.9425, -118.4081)
    
    route = calculate_flight_route(lax, lax)
    assert route is None

def test_coordinate_bug_fix():
    """
    CRITICAL TEST: Verify destination coordinates are NOT copied from origin.
    This was a bug in the original single-file version.
    """
    origin = Airport("LAX", "Los Angeles", "Los Angeles", "USA", 33.94, -118.41)
    dest = Airport("JFK", "New York", "New York", "USA", 40.64, -73.78)
    
    route = calculate_flight_route(origin, dest)
    
    # Verify destination coordinates are correct (NOT origin's)
    assert abs(route.destination.latitude - 40.64) < 0.01
    assert abs(route.destination.longitude - (-73.78)) < 0.01
    
    # Verify origin coordinates are correct
    assert abs(route.origin.latitude - 33.94) < 0.01
    assert abs(route.origin.longitude - (-118.41)) < 0.01