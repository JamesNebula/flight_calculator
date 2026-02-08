"""
Flight Path Distance Calculator - Streamlit Frontend
"""
import streamlit as st
import os
from pathlib import Path

# Add project root to path BEFORE importing our modules
project_root = Path(__file__).parent
if str(project_root) not in os.sys.path:
    os.sys.path.insert(0, str(project_root))

from models.airport import Airport, FlightRoute
from services.airport_loader import load_airport_database, AIRPORTS_CSV
from services.route_calculator import calculate_flight_route, validate_airport_codes

# Page configuration
st.set_page_config(
    page_title="✈️ Flight Path Calculator",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
    }
    .route-info {
        background-color: #c1e1d1;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .debug-info {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✈️ Flight Path Distance Calculator</p>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="color: #666; font-size: 1.1rem;">
        Calculate great-circle distances, bearings, and flight times between global airports
    </p>
</div>
""", unsafe_allow_html=True)

# Load airport database - NO CACHING for debugging
airports = load_airport_database()

# DEBUG: Show what happened during load
if 'debug_load' not in st.session_state:
    st.session_state.debug_load = f"Loaded {len(airports)} airports from: {AIRPORTS_CSV.absolute()}"

if not airports:
    st.error("❌ Unable to load airport database. Please check the data/airports.csv file.")
    st.markdown(f'<div class="debug-info">DEBUG: {st.session_state.debug_load}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="debug-info">Working directory: {Path.cwd().absolute()}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="debug-info">Airport CSV path: {AIRPORTS_CSV.absolute()}</div>', unsafe_allow_html=True)
    st.stop()

# Sidebar for airport selection
st.sidebar.header("📍 Select Route")
st.sidebar.markdown("---")

# Create sorted list of airport options for dropdowns
airport_options = [f"{code} - {airport.city}, {airport.country}" 
                   for code, airport in sorted(airports.items())]

# Origin selection
origin_selection = st.sidebar.selectbox(
    "🛫 Origin Airport",
    airport_options,
    index=0  # Default to first airport
)

# Destination selection
dest_selection = st.sidebar.selectbox(
    "🛬 Destination Airport",
    airport_options,
    index=min(1, len(airport_options)-1)  # Safe default
)

# Extract airport codes from selection strings
origin_code = origin_selection.split(" - ")[0]
dest_code = dest_selection.split(" - ")[0]

# Calculate route button
st.sidebar.markdown("---")
if st.sidebar.button("✈️ Calculate Route", type="primary", use_container_width=True):
    # Validate and calculate
    origin_airport, dest_airport = validate_airport_codes(origin_code, dest_code, airports)
    
    if origin_airport and dest_airport:
        route = calculate_flight_route(origin_airport, dest_airport)
        
        if route:
            # Store route in session state for display
            st.session_state.route = route
            st.session_state.error = None
        else:
            st.session_state.error = "Failed to calculate route"
    else:
        st.session_state.error = "Invalid airport selection"

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Route Information Section
    st.subheader("🗺️ Route Information")
    
    if 'route' in st.session_state:
        route = st.session_state.route
        
        # Origin details
        st.markdown(f"""
        <div class="route-info">
            <h4>🛫 Departure: {route.origin.name}</h4>
            <p><strong>Code:</strong> {route.origin.code} | 
               <strong>City:</strong> {route.origin.city} | 
               <strong>Country:</strong> {route.origin.country}</p>
            <p><strong>Coordinates:</strong> {route.origin.latitude:.4f}°, {route.origin.longitude:.4f}°</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Destination details
        st.markdown(f"""
        <div class="route-info">
            <h4>🛬 Arrival: {route.destination.name}</h4>
            <p><strong>Code:</strong> {route.destination.code} | 
               <strong>City:</strong> {route.destination.city} | 
               <strong>Country:</strong> {route.destination.country}</p>
            <p><strong>Coordinates:</strong> {route.destination.latitude:.4f}°, {route.destination.longitude:.4f}°</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif 'error' in st.session_state and st.session_state.error:
        st.error(f"❌ {st.session_state.error}")
    else:
        st.info("👆 Select airports in the sidebar and click 'Calculate Route' to see results")

with col2:
    # Quick Stats Section
    st.subheader("📊 Quick Stats")
    
    if 'route' in st.session_state:
        route = st.session_state.route
        
        # Distance metrics
        st.metric(
            label="Distance (Miles)",
            value=f"{route.distance_miles:,.2f} mi"
        )
        
        st.metric(
            label="Distance (Kilometers)",
            value=f"{route.distance_km:,.2f} km"
        )
        
        st.metric(
            label="Distance (Nautical Miles)",
            value=f"{route.distance_nautical_miles:,.2f} NM"
        )
        
        st.markdown("---")
        
        # Navigation metrics
        st.metric(
            label="Initial Bearing",
            value=f"{route.bearing_degrees}°"
        )
        
        st.metric(
            label="Compass Direction",
            value=route.compass_direction
        )
        
        # Flight time
        hours, minutes = route.get_duration_minutes()
        st.metric(
            label="Estimated Flight Time",
            value=f"{hours}h {minutes}m",
            delta=f"({route.estimated_flight_hours:.2f} hours total)"
        )

# Detailed Analysis Section (full width)
if 'route' in st.session_state:
    st.markdown("---")
    st.subheader("📈 Detailed Analysis")
    
    route = st.session_state.route
    
    # Create three columns for detailed info
    dcol1, dcol2, dcol3 = st.columns(3)
    
    with dcol1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📏 Distance Breakdown")
        st.markdown(f"""
        - **Miles:** {route.distance_miles:,.2f}
        - **Kilometers:** {route.distance_km:,.2f}
        - **Nautical Miles:** {route.distance_nautical_miles:,.2f}
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with dcol2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🧭 Navigation")
        st.markdown(f"""
        - **Initial Bearing:** {route.bearing_degrees}°
        - **Compass Direction:** {route.compass_direction}
        - **Heading:** Northeast bound
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with dcol3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### ⏱️ Flight Time")
        hours, minutes = route.get_duration_minutes()
        st.markdown(f"""
        - **Duration:** {hours}h {minutes}m
        - **Total Hours:** {route.estimated_flight_hours:.2f}
        - **Speed Assumption:** 500 mph
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer with debug info in dev mode
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>✈️ Flight Path Distance Calculator</strong></p>
    <p>Built with Python • Streamlit</p>
</div>
""", unsafe_allow_html=True)

