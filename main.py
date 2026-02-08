
"""
Flight Path Distance Calculator 
"""
import os
import sys

# Add project root to path for clean imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.airport_loader import load_airport_database
from services.route_calculator import calculate_flight_route
from utils.display import display_batch_analysis
from utils.file_io import save_route_analysis
from cli import interactive_route_planner
from models.airport import BatchAnalysis

# Popular international routes for demo
POPULAR_ROUTES = [
    ("LAX", "JFK"),  # US Transcontinental
    ("LHR", "JFK"),  # Transatlantic
    ("NRT", "LAX"),  # Transpacific
    ("SYD", "LAX"),  # US-Australia
    ("DXB", "LHR"),  # Middle East-Europe
    ("CDG", "JFK"),  # Europe-US
]

def analyze_batch_routes(route_pairs, airports):
    """Analyze multiple routes and generate summary statistics."""
    routes = []
    total_distance = 0.0
    total_time = 0.0
    
    print("\n  Analyzing multiple routes...")
    print("-" * 50)
    
    for i, (origin_code, dest_code) in enumerate(route_pairs, 1):
        print(f"  Route {i}/{len(route_pairs)}: {origin_code} → {dest_code}")
        
        if origin_code not in airports or dest_code not in airports:
            print(f"     Skipping invalid route: {origin_code} → {dest_code}")
            continue
        
        route = calculate_flight_route(airports[origin_code], airports[dest_code])
        if route:
            routes.append(route)
            total_distance += route.distance_miles
            total_time += route.estimated_flight_hours
    
    if not routes:
        raise ValueError("No valid routes to analyze")
    
    # Sort by distance for min/max identification
    routes_sorted = sorted(routes, key=lambda r: r.distance_miles)
    
    return BatchAnalysis(
        routes=routes,
        total_distance_miles=total_distance,
        average_distance_miles=total_distance / len(routes),
        total_flight_time_hours=total_time,
        average_flight_time_hours=total_time / len(routes),
        shortest_route=routes_sorted[0],
        longest_route=routes_sorted[-1]
    )

def main():
    """Main program entry point."""
    print("\n" + "✈️ " * 25)
    print("   FLIGHT PATH DISTANCE CALCULATOR")
    print("✈️ " * 25)
    
    # Load airport database
    airports = load_airport_database()
    if not airports:
        print("  Exiting due to airport database error")
        return
    
    # Demo batch analysis
    print("\n  Analyzing popular international routes...")
    try:
        batch_analysis = analyze_batch_routes(POPULAR_ROUTES, airports)
        display_batch_analysis(batch_analysis)
        
        # Save results
        save_route_analysis(batch_analysis, "output/popular_routes_analysis.txt")
        
    except Exception as e:
        print(f"   Batch analysis skipped: {e}")
    
    # Offer interactive mode
    while True:
        print("\n" + "-"*50)
        choice = input("  Calculate a custom route? (y/n): ").strip().lower()
        if choice != 'y':
            break
        interactive_route_planner()
    
    print("\n  Flight analysis complete! Safe travels!  \n")

if __name__ == "__main__":
    main()