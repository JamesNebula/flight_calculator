# ✈️ Flight Path Distance Calculator

**[▶️ Try the Live Demo]((https://flightcalculator.streamlit.app/))**

A professional-grade tool for calculating great-circle distances, bearings, and flight times between global airports using the Haversine formula.

## ✨ Key Features

- **Accurate geodesic calculations** using the Haversine formula
- **Multi-unit distance support**: miles, kilometers, nautical miles
- **Navigation data**: initial bearing and compass direction
- **Flight time estimation** based on commercial jet speeds
- **Batch analysis** with statistics (shortest/longest routes, averages)
- **Interactive Streamlit UI** with responsive design
- **Clean CLI interface** with interactive route planning

## Architecture 
```bash
flight_calculator/
├── streamlit_app.py # Interactive web frontend
├── main.py # CLI entry point
├── models/ # Data structures (Airport, FlightRoute)
├── services/ # Business logic (calculations, validation)
├── utils/ # Display helpers and file I/O
├── tests/ # Pytest validation 
├── data/ # Airport database (CSV)
└── output/ # Generated reports
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit UI 
streamlit run streamlit_app.py

# Or run the CLI version
python main.py

# Run tests
pytest tests/ -v
