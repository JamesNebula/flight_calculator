"""Interactive command-line interface for flight planning."""
import os
from services.airport_loader import load_airport_database
from services.route_calculator import validate_airport_codes, calculate_flight_route
from utils.display import display_route_info, display_available_airports
from utils.file_io import save_route_analysis

def interactive_route_planner():
    """Run interactive flight route planning session."""
    print("\n   INTERACTIVE FLIGHT ROUTE PLANNER")
    print("="*50)
    
    # Load airport database
    airports = load_airport_database()
    if not airports:
        print("  Cannot proceed without airport database")
        return
    
    # Show available airports
    display_available_airports(airports)
    
    # Get user input
    print("\n" + "-"*50)
    origin_code = input("Enter origin airport code (e.g., LAX): ").strip().upper()
    dest_code = input("Enter destination airport code (e.g., JFK): ").strip().upper()
    
    # Validate and get airport objects
    origin, destination = validate_airport_codes(origin_code, dest_code, airports)
    if not origin or not destination:
        return
    
    # Calculate route
    route = calculate_flight_route(origin, destination)
    if not route:
        return
    
    # Display results
    display_route_info(route)
    
    # Offer to save
    save_choice = input("\n💾 Save this route analysis to file? (y/n): ").strip().lower()
    if save_choice == 'y':
        timestamp = int(os.time.time()) # type: ignore
        filename = f"output/route_{origin.code}_to_{destination.code}_{timestamp}.txt"
        save_route_analysis(route, filename)