"""
Battlefield Configuration
"""

# Battlefield Dimensions (km)
BATTLEFIELD_SIZE = 400

# Default Simulation Parameters
DEFAULT_TANKS = 20
DEFAULT_UAVS = 4
DEFAULT_TANK_SPEED = 3          # km/min
DEFAULT_ISR_DELAY = 10          # minutes

# Detection & Strike
DETECTION_RADIUS = 40           # km
STRIKE_RADIUS = 15              # km

# Artillery Position
ARTILLERY_X = BATTLEFIELD_SIZE / 2
ARTILLERY_Y = BATTLEFIELD_SIZE / 2

# Monte Carlo
DEFAULT_SIMULATIONS = 10000