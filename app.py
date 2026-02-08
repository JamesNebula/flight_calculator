import math
import csv
import os
from datetime import datetime

EARTHS_RADIUS_MILES = 3959
EARTH_RADIUS_KM = 6371
EARTH_RADIUS_NAUTICAL_MILES = 3440

AIRPORT_DATA = [
    ["Airport_Code", "Airport_Name", "City", "Country", "Latitude", "Longitude"],
    ["LAX", "Los Angeles International", "Los Angeles", "USA", "33.9425", "-118.4081"],
    ["JFK", "John F. Kennedy International", "New York", "USA", "40.6413", "-73.7781"],
    ["LHR", "London Heathrow", "London", "UK", "51.4700", "-0.4543"],
    ["NRT", "Tokyo Narita", "Tokyo", "Japan", "35.7647", "140.3864"],
    ["SYD", "Sydney Kingsford Smith", "Sydney", "Australia", "-33.9399", "151.1753"],
    ["DXB", "Dubai International", "Dubai", "UAE", "25.2532", "55.3657"],
    ["CDG", "Charles de Gaulle", "Paris", "France", "49.0097", "2.5479"],
    ["FRA", "Frankfurt am Main", "Frankfurt", "Germany", "50.0379", "8.5622"],
    ["SIN", "Singapore Changi", "Singapore", "Singapore", "1.3644", "103.9915"],
    ["ORD", "O'Hare International", "Chicago", "USA", "41.9742", "-87.9073"]
]

def create_airport_data_file(filename="airports.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(AIRPORT_DATA)
    print(f"Airport database '{filename}' created successfully!")
    
def load_airport_database(filename):
    airports = {}
    
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                airports[row['Airport_Code']] = {
                    'name': row['Airport_Name'],
                    'city': row['City'],
                    'country': row['Country'],
                    'latitude': float(row['Latitude']),
                    'longitude': float(row['Longitude'])
                }
                
        print(f"Loaded {len(airports)} airports into database!")
        return airports
    
    except FileNotFoundError:
        print(f"Error: Airport database '{filename} not found!'")
        return {}
    except ValueError as e:
        print(f"Error: Invalid coordinate data in file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading airports: {e}")
        return {}
    
def degrees_to_radians(degrees):
    return degrees * math.pi / 180

def calculate_great_circle_distance(lat1, lon1, lat2, lon2, unit='miles'):
    #convert coordinates to radians 
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    lon2_rad = degrees_to_radians(lon2)
    
    # calculate the differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    #Haversine formula --> a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(dlon / 2) ** 2) 
    
    # c = 2 × atan2(√a, √(1−a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # choose earths radius based on a desired unit
    if unit == 'km': 
        radius = EARTH_RADIUS_KM
    elif unit == 'nautical_miles':
        radius = EARTH_RADIUS_NAUTICAL_MILES
    else:
        radius = EARTHS_RADIUS_MILES
        
    # distance = Radius x c
    distance = radius * c
    
    return round(distance, 2)

def calculate_inital_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the initial compass bearing from point 1 to point 2.
    
    WHY PILOTS NEED BEARING:
    - Tells them what compass direction to fly
    - Essential for navigation planning
    - Shows you're thinking beyond just distance
    """
    
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    dlon_rad = degrees_to_radians(lon2 - lon1)
    
    # Formula for initial bearing
    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad) - 
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad))
    
    bearing_rad = math.atan2(y, x)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360
    
    return round(bearing_deg, 1)

def get_compass_direction(bearing):
    # Converts numeric bearing to compass direction. - Humans think in "Northeast" not "45.7 degrees"
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    
    # Each direction covers 22.5 degrees
    index = round(bearing / 22.5) % 16
    return directions[index]

def calculate_flight_route(origin_code, destination_code, airports):
    #Calculates complete flight route information.
    # - Returns everything needed for one flight
    
    #validate airport codes
    if origin_code not in airports:
        print(f"Origin airport '{origin_code}' not found in database!")
        return None
    if destination_code not in airports:
        print(f"Destination airport '{destination_code}' not found in database!")
        return None
    if origin_code == destination_code:
        print(f"Origin and destination cannot be the same!")
        
    # get airport info
    origin = airports[origin_code]
    destination = airports[destination_code]
    
    #calculate flight distance
    distance_miles = calculate_great_circle_distance(
        origin['latitude'], origin['longitude'], 
        destination['latitude'], destination['longitude'],
        'miles'
    )
    
    distance_km = calculate_great_circle_distance(
        origin['latitude'], origin['longitude'],
        destination['latitude'], destination['longitude'],
        'km'
    )
    
    distance_nm = calculate_great_circle_distance(
        origin['latitude'], origin['longitude'],
        destination['latitude'], destination['longitude'],
        'nautical_miles'
    )
    
    # calculate bearing and compass direction
    bearing = calculate_inital_bearing(
        origin['latitude'], origin['longitude'],
        destination['latitude'], destination['longitude']
    )
    
    compass_direction = get_compass_direction(bearing)
    estimated_flight_hours = distance_miles / 500
    flight_hours = int(estimated_flight_hours)
    flight_minutes = int((estimated_flight_hours - flight_hours) * 60)
    
    return {
        'origin': {
            'code': origin_code,
            'name': origin['name'],
            'city': origin['city'],
            'country': origin['country'],
            'coordinates': (origin['latitude'], origin['longitude']) 
        },
        'destination': {
            'code': destination_code,
            'name': destination['name'],
            'city': destination['city'],
            'country': destination['country'],
            'coordinates': (origin['latitude'], origin['longitude'])
        },
        'distance': {
            'miles': distance_miles,
            'kilometers': distance_km,
            'nautical_miles': distance_nm
        },
        'bearing': bearing,
        'compass_direction': compass_direction,
        'estimated_flight_time': {
            'hours': flight_hours,
            'minutes': flight_minutes,
            'total_hours': round(estimated_flight_hours, 2)
        }
    }
    
def display_route_info(route_info):
    # Displays formatted flight route information.
    if not route_info:
        return
    
    print("\n" + "="*70)
    print("✈️  FLIGHT ROUTE ANALYSIS")
    print("=" * 70)
    
    #route summary
    origin = route_info['origin']
    destination = route_info['destination']
    
    print(f"\n🛫 DEPARTURE: {origin['code']} - {origin['name']}")
    print(f"   📍 {origin['city']}, {origin['country']}")
    print(f"   🌐 {origin['coordinates'][0]:.4f}°, {origin['coordinates'][1]:.4f}°")
    
    print(f"\n🛬 ARRIVAL: {destination['code']} - {destination['name']}")
    print(f"   📍 {destination['city']}, {destination['country']}")
    print(f"   🌐 {destination['coordinates'][0]:.4f}°, {destination['coordinates'][1]:.4f}°")
    
    # Distance information
    dist = route_info['distance']
    print(f"\n📏 DISTANCE:")
    print(f"   🇺🇸 {dist['miles']:,} miles")
    print(f"   🌍 {dist['kilometers']:,} kilometers")
    print(f"   ⚓ {dist['nautical_miles']:,} nautical miles")
    
    # Navigation information
    print(f"\n🧭 NAVIGATION:")
    print(f"   Initial Bearing: {route_info['bearing']}°")
    print(f"   Compass Direction: {route_info['compass_direction']}")
    
    # Flight time estimate
    flight_time = route_info['estimated_flight_time']
    print(f"\n⏱️  ESTIMATED FLIGHT TIME:")
    print(f"   Duration: {flight_time['hours']}h {flight_time['minutes']}m")
    print(f"   Total Hours: {flight_time['total_hours']}")
    print(f"   (Based on 500 mph average commercial speed)")
    
    print("\n" + "="*70)
    
def batch_route_analysis(route_list, airports):
    #Analyzes multiple routes and finds interesting patterns
    
    routes_analyzed = []
    total_distance = 0
    total_flight_time = 0
    
    print("\n🔍 ANALYZING MULTIPLE ROUTES...")
    print("-" * 50)

    for i, (origin, destination) in enumerate(route_list, 1):
        print(f"Calculating route {i}: {origin} → {destination}")
        
        route_info = calculate_flight_route(origin, destination, airports)
        if route_info:
            routes_analyzed.append(route_info)
            total_distance += route_info['distance']['miles']
            total_flight_time += route_info['estimated_flight_time']['total_hours']
            
    if not routes_analyzed:
        return {}
    
    # Find longest and shortest routes
    routes_by_distance = sorted(routes_analyzed, key=lambda r: r['distance']['miles'])
    shortest_route = routes_by_distance[0]
    longest_route = routes_by_distance[-1]
    
    #calculate averages
    avg_distance = total_distance / len(routes_analyzed)
    avg_flight_time = total_flight_time / len(routes_analyzed)
    
    return {
        'routes_analyzed': routes_analyzed,
        'total_routes': len(routes_analyzed),
        'shortest_route': shortest_route,
        'longest_route': longest_route,
        'total_distance_miles': round(total_distance, 2),
        'average_distance_miles': round(avg_distance, 2),
        'total_flight_time_hours': round(total_flight_time, 2),
        'average_flight_time_hours': round(avg_flight_time, 2)
    }
    
def display_batch_analysis(analysis):
    if not analysis:
        print("❌ No routes to analyze")
        return
    
    print("\n" + "="*70)
    print("📊 BATCH ROUTE ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   Total Routes Analyzed: {analysis['total_routes']}")
    print(f"   Total Distance: {analysis['total_distance_miles']:,} miles")
    print(f"   Average Distance: {analysis['average_distance_miles']:,} miles")
    print(f"   Total Flight Time: {analysis['total_flight_time_hours']:.1f} hours")
    print(f"   Average Flight Time: {analysis['average_flight_time_hours']:.1f} hours")
    
    #shortest route
    shortest = analysis['shortest_route']
    print(f"\n🏃 SHORTEST ROUTE:")
    print(f"   {shortest['origin']['code']} → {shortest['destination']['code']}")
    print(f"   Distance: {shortest['distance']['miles']:,} miles")
    print(f"   Flight Time: {shortest['estimated_flight_time']['total_hours']:.1f} hours")
    
    # Longest route
    longest = analysis['longest_route']
    print(f"\n🛣️  LONGEST ROUTE:")
    print(f"   {longest['origin']['code']} → {longest['destination']['code']}")
    print(f"   Distance: {longest['distance']['miles']:,} miles")
    print(f"   Flight Time: {longest['estimated_flight_time']['total_hours']:.1f} hours")
    
def save_routes_to_file(analysis, filename="flight_route_analysis.txt"):
    try:
        with open(filename, 'w') as file:
            file.write("FLIGHT ROUTE ANALYSIS REPORT\n")
            file.write("="*50 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if analysis.get('routes_analyzed'):
                file.write("INDIVIDUAL ROUTES:\n")
                file.write("-" * 30 + "\n")
                
                for route in analysis['routes_analyzed']:
                    origin = route['origin']
                    dest = route['destination']
                    
                    file.write(f"Route: {origin['code']} to {dest['code']}\n")
                    file.write(f"From: {origin['city']}, {origin['country']}\n")
                    file.write(f"To: {dest['city']}, {dest['country']}\n")
                    file.write(f"Distance: {route['distance']['miles']:,} miles\n")
                    file.write(f"Bearing: {route['bearing']}° ({route['compass_direction']})\n")
                    file.write(f"Est. Flight Time: {route['estimated_flight_time']['total_hours']:.1f} hours\n")
                    file.write("-" * 30 + "\n")
                    
            file.write(f"\nSUMMARY:\n")
            file.write(f"Total Routes: {analysis.get('total_routes', 0)}\n")
            file.write(f"Total Distance: {analysis.get('total_distance_miles', 0):,.0f} miles\n")
            
        print(f"✅ Route analysis saved to '{filename}'")
        
    except Exception as e:
        print(f"❌ Error saving analysis: {e}")
        
def interactive_route_planner():
    #Interactive mode for single route planning.
    print("\n✈️  INTERACTIVE FLIGHT ROUTE PLANNER")
    print("="*50)
    
    if not os.path.exists('airports.csv'):
        create_airport_data_file()
        
    airports = load_airport_database('airports.csv')
    if not airports:
        return
    
    # show available airports
    print("\n📍 AVAILABLE AIRPORTS:")
    for code, info in sorted(airports.items()):
        print(f"   {code}: {info['city']}, {info['country']}")
        
    # get user input
    print("\n" + "-" * 50)
    origin = input("Enter origin airport code (e.g, LAX)").upper().strip()
    destination = input("Enter destination airport code (e.g, JFK)").upper().strip()
    
    # Calculate and display route
    route_info = calculate_flight_route(origin, destination, airports)
    if route_info:
        display_route_info(route_info)
        
        #Ask if user wants to save
        save_choice = input("\nSave this route analysis? (y/n): ").lower().strip()
        if save_choice == 'y':
            filename = f"route_{origin}_to_{destination}.txt"
            save_routes_to_file({'routes_analyzed': [route_info], 'total_routes': 1}, filename)
            
def main():
    """
    Main program function - demonstrates both batch and interactive modes.
    
    NOTICE THE SAME STRUCTURE AS DAY 1:
    - Setup data
    - Process data
    - Display results
    - Save results
    
    But now with more complex mathematics and user interaction!
    """
    print("✈️  Flight Path Distance Calculator")
    print("="*50)
    
    if not os.path.exists("airports.csv"):
        print("📝 Creating airport database...")
        create_airport_data_file()
        
    airports = load_airport_database('airports.csv')
    if not airports:
        return
    
    # Demo: Batch analysis of popular routes
    print("\n🌍 ANALYZING POPULAR INTERNATIONAL ROUTES...")
    popular_routes = [
        ("LAX", "JFK"),  # US Transcontinental
        ("LHR", "JFK"),  # Transatlantic
        ("NRT", "LAX"),  # Transpacific
        ("SYD", "LAX"),  # US-Australia
        ("DXB", "LHR"),  # Middle East-Europe
        ("CDG", "JFK"),  # Europe-US
    ]
    
    batch_analysis = batch_route_analysis(popular_routes, airports)
    display_batch_analysis(batch_analysis)
    
    #save batch analysis
    if batch_analysis:
        save_routes_to_file(batch_analysis, "popular_routes_analysis.txt")
        
    #interactive mode 
    while True:
        choice = input("\n🤔 Calculate a custom route? (y/n): ").lower().strip()  
        if choice == 'n':
            break
        interactive_route_planner()
        
    print("\n✅ Flight analysis complete! Safe travels! ✈️")
    
if __name__ == "__main__":
    main()  