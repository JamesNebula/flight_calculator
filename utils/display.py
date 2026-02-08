"""Presentation logic for flight route information."""

def display_route_info(route):
    """Display formatted flight route information."""
    print("\n" + "="*70)
    print("   FLIGHT ROUTE ANALYSIS")
    print("="*70)
    
    # Origin details
    print(f"\n  DEPARTURE: {route.origin.code} - {route.origin.name}")
    print(f"     {route.origin.city}, {route.origin.country}")
    print(f"     {route.origin.latitude:.4f}°, {route.origin.longitude:.4f}°")
    
    # Destination details (FIXED: uses destination coordinates)
    print(f"\n  ARRIVAL: {route.destination.code} - {route.destination.name}")
    print(f"     {route.destination.city}, {route.destination.country}")
    print(f"     {route.destination.latitude:.4f}°, {route.destination.longitude:.4f}°")
    
    # Distance information
    print(f"\n  DISTANCE:")
    print(f"    {route.distance_miles:,.2f} miles")
    print(f"    {route.distance_km:,.2f} kilometers")
    print(f"    {route.distance_nautical_miles:,.2f} nautical miles")
    
    # Navigation information
    print(f"\n  NAVIGATION:")
    print(f"   Initial Bearing: {route.bearing_degrees}°")
    print(f"   Compass Direction: {route.compass_direction}")
    
    # Flight time estimate
    hours, minutes = route.get_duration_minutes()
    print(f"\n  ESTIMATED FLIGHT TIME:")
    print(f"   Duration: {hours}h {minutes}m")
    print(f"   Total Hours: {route.estimated_flight_hours:.2f}")
    print(f"   (Based on 500 mph average commercial speed)")
    
    print("\n" + "="*70)


def display_batch_analysis(analysis):
    """Display summary statistics for batch route analysis."""
    if not analysis.routes:
        print("  No routes to analyze")
        return
    
    print("\n" + "="*70)
    print("BATCH ROUTE ANALYSIS RESULTS")
    print("="*70)
    
    # Summary statistics
    print(f"\nUMMARY STATISTICS:")
    print(f"   Total Routes Analyzed: {analysis.get_total_routes()}")
    print(f"   Total Distance: {analysis.total_distance_miles:,.2f} miles")
    print(f"   Average Distance: {analysis.average_distance_miles:,.2f} miles")
    print(f"   Total Flight Time: {analysis.total_flight_time_hours:.2f} hours")
    print(f"   Average Flight Time: {analysis.average_flight_time_hours:.2f} hours")
    
    # Shortest route
    if analysis.shortest_route:
        print(f"\nSHORTEST ROUTE:")
        print(f"   {analysis.shortest_route.origin.code} → {analysis.shortest_route.destination.code}")
        print(f"   Distance: {analysis.shortest_route.distance_miles:,.2f} miles")
        print(f"   Flight Time: {analysis.shortest_route.estimated_flight_hours:.2f} hours")
    
    # Longest route
    if analysis.longest_route:
        print(f"\nLONGEST ROUTE:")
        print(f"   {analysis.longest_route.origin.code} → {analysis.longest_route.destination.code}")
        print(f"   Distance: {analysis.longest_route.distance_miles:,.2f} miles")
        print(f"   Flight Time: {analysis.longest_route.estimated_flight_hours:.2f} hours")
    
    print("\n" + "="*70)


def display_available_airports(airports):
    """Display available airports in a clean, sorted format."""
    print("\nAVAILABLE AIRPORTS:")
    for code in sorted(airports.keys()):
        airport = airports[code]
        print(f"   • {code:4s} | {airport.city:<20s} | {airport.country}")