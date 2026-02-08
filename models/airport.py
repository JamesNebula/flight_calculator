"""simple data models for airports and flight routes"""

class Airport:
    # Represents an airport with location data
    def __init__(self, code, name, city, country, latitude, longitude):
        self.code = code
        self.name = name
        self.city = city 
        self.country = country
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def get_coordinates(self):
        # Get airport coords as (lat, long) tuple
        return (self.latitude, self.longitude)
    
    def __str__(self) -> str:
        return f"{self.code}: {self.city}, {self.country}"
    
class FlightRoute:
    # Complete flight route analysis between two airports
    def __init__(self, origin, destination, distance_miles, distance_km,
                 distance_nautical_miles, bearing_degrees, compass_direction,
                 estimated_flight_hours):
        
        self.origin = origin
        self.destination = destination
        self.distance_miles = distance_miles
        self.distance_km = distance_km
        self.distance_nautical_miles = distance_nautical_miles
        self.bearing_degrees = bearing_degrees
        self.compass_direction = compass_direction
        self.estimated_flight_hours = estimated_flight_hours

    def get_duration_minutes(self):
        # Return flight time as (hours, minutes) tuple
        hours = int(self.estimated_flight_hours)
        minutes = int((self.estimated_flight_hours - hours) * 60)
        return hours, minutes
    
class BatchAnalysis:
    # Results from analyzing multiple flight routes

    def __init__(self, routes, total_distance_miles, average_distance_miles,
                 total_flight_time_hours, average_flight_time_hours,
                 shortest_route, longest_route):
        self.routes = routes
        self.total_distance_miles = total_distance_miles
        self.average_distance_miles = average_distance_miles
        self.total_flight_time_hours = total_flight_time_hours
        self.average_flight_time_hours = average_flight_time_hours
        self.shortest_route = shortest_route
        self.longest_route = longest_route

    def get_total_routes(self):
        return len(self.routes)
        
        
    
