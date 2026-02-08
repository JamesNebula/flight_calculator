"""Earth geometry constants for distance calculations."""

EARTH_RADIUS_MILES = 3959.0
EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_NAUTICAL_MILES = 3440.0

# 16-point compass directions
COMPASS_DIRECTIONS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]
COMPASS_SEGMENT_SIZE = 22.5  # degrees per segment