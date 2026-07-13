import random


def random_coordinate(max_size):
    """
    Generate a random coordinate inside battlefield.
    """
    return random.uniform(0, max_size)


def clamp(value, minimum, maximum):
    """
    Restrict value within limits.
    """
    return max(minimum, min(value, maximum))


def success_percentage(destroyed, total):
    """
    Calculate destruction percentage.
    """
    if total == 0:
        return 0

    return round((destroyed / total) * 100, 2)