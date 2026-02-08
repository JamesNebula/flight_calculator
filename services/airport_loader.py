"""Airport database loading and management with robust path handling."""
import csv
import os
from pathlib import Path
from models.airport import Airport

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AIRPORTS_CSV = DATA_DIR / "airports.csv"

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

def create_airport_data_file(filepath=AIRPORTS_CSV):
    """Create default airport database CSV file."""
    try:
        # Ensure data directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(DEFAULT_AIRPORT_DATA)
        print(f" Airport database created at '{filepath.absolute()}'")
        return True
    except Exception as e:
        print(f" Error creating airport database: {e}")
        import traceback
        traceback.print_exc()
        return False

def load_airport_database(filepath=AIRPORTS_CSV):
    """
    Load airport database from CSV file using absolute paths.
    
    Returns:
        Dictionary mapping airport codes to Airport objects
    """
    # Auto-generate if file doesn't exist
    if not filepath.exists():
        print(f"   Airport database not found at '{filepath.absolute()}'. Creating default database...")
        create_airport_data_file(filepath)
    
    airports = {}
    
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            
            # DEBUG: Show actual path and fieldnames
            print(f"DEBUG: Loading airports from: {filepath.absolute()}")
            print(f"DEBUG: CSV fieldnames = {reader.fieldnames}")
            
            for row in reader:
                try:
                    airport = Airport(
                        code=row['Airport_Code'].strip().upper(),
                        name=row['Airport_Name'].strip(),     
                        city=row['City'].strip(),
                        country=row['Country'].strip(),
                        latitude=row['Latitude'].strip(),
                        longitude=row['Longitude'].strip()
                    )
                    airports[airport.code] = airport
                except (ValueError, KeyError) as e:
                    print(f"   Skipping invalid airport record: {row.get('Airport_Code', 'UNKNOWN')} - Error: {e}")
                    continue
        
        print(f"  Loaded {len(airports)} airports from '{filepath.name}'")
        return airports
        
    except FileNotFoundError:
        print(f"  Airport database '{filepath.absolute()}' not found!")
        return {}
    except Exception as e:
        print(f"  Unexpected error loading airports: {e}")
        import traceback
        traceback.print_exc()
        return {}