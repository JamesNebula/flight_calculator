"""Airport database loading and management."""
import csv
import os
from models.airport import Airport

# Default airport data (for auto-generation)
DEFAULT_AIRPORT_DATA = [
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

def create_airport_data_file(filename='data/airports.csv'):
    #create default airport database CSV
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(DEFAULT_AIRPORT_DATA)
        print(f"Airport database created at '{filename}'")
        return True
    except Exception as e:
        print(f"Error creating airport database: {e}")
        return False
    
def load_airport_database(filename='data/airports.csv'):
    # Load aiport database from csv file
    # Returns: dictionary mapping airport codes to airport objects

    if not os.path.exists(filename):
        print(f"Airport database not found. Creating default database...")
        create_airport_data_file(filename)

    airports = {}

    try: 
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader: 
                try:
                    airport = Airport(
                        code=row['Airport_Code'].strip().upper(),
                        name=row['Airport_name'].strip(),
                        city=row['City'].strip(),
                        country=row['Country'].strip(),
                        latitude=row['Latitude'].strip(),
                        longitude=row['Longitude'].strip()
                    )
                    airports[airport.code] = airport
                except (ValueError, KeyError) as e:
                    print(f"skipping invalid airport record: {row.get('Airport_Code', 'UNKNOWN')} - {e}")
                    continue
        print(f"Loaded {len(airports)} airports from '{filename}'")
    except FileNotFoundError:
        print(f"Airport database '{filename}' not found!")
        return {}
    except Exception as e:
        print(f"Unexpected error loading airports: {e}")