import math
from config import DETECTION_RADIUS


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def detect(uav, tank):
    """
    Returns True if UAV detects the tank.
    """

    d = distance(uav.x, uav.y, tank.x, tank.y)

    if d <= DETECTION_RADIUS:
        return True

    return False

