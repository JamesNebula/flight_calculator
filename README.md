# ✈️ Flight Path Distance Calculator

A professional-grade tool for calculating great-circle distances, bearings, and flight times between global airports using the Haversine formula.

![Flight Calculator Demo](demo.png)

## ✨ Key Features

- **Accurate geodesic calculations** using the Haversine formula
- **Multi-unit distance support**: miles, kilometers, nautical miles
- **Navigation data**: initial bearing and compass direction
- **Flight time estimation** based on commercial jet speeds
- **Batch analysis** with statistics (shortest/longest routes, averages)
- **Clean CLI interface** with interactive route planning
- **Professional architecture** demonstrating software engineering best practices

## 🏗️ Architecture Highlights
```bash
flight_calculator/
├── config/ # Constants and configuration
├── models/ # Dataclasses (Airport, FlightRoute)
├── services/ # Business logic (calculations, validation)
├── utils/ # Presentation and I/O helpers
└── data/ # Externalized airport database
```

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/flight-calculator.git
cd flight-calculator

# Run the calculator (no installation needed - standard library only)
python main.py