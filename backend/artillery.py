import math
from config import STRIKE_RADIUS


def calculate_distance(x1, y1, x2, y2):
    """
    Calculate Euclidean distance between two points.
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def strike(target_x, target_y, tank):
    """
    Simulate an artillery strike.

    Parameters:
        target_x (float): Detected tank x-coordinate
        target_y (float): Detected tank y-coordinate
        tank (Tank): Current tank object

    Returns:
        bool: True if strike destroys the tank, else False
    """

    distance = calculate_distance(
        target_x,
        target_y,
        tank.x,
        tank.y
    )

    if distance <= STRIKE_RADIUS:
        return True

    return False