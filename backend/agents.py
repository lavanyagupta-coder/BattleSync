import random
from config import BATTLEFIELD_SIZE


class Tank:
    def __init__(self, tank_id):
        self.id = tank_id
        self.x = random.uniform(0, BATTLEFIELD_SIZE)
        self.y = random.uniform(0, BATTLEFIELD_SIZE)
        self.alive = True

    def position(self):
        return (round(self.x, 2), round(self.y, 2))

    def __repr__(self):
        return f"Tank {self.id}: ({self.x:.2f}, {self.y:.2f})"


class UAV:
    def __init__(self, uav_id):
        self.id = uav_id
        self.x = random.uniform(0, BATTLEFIELD_SIZE)
        self.y = random.uniform(0, BATTLEFIELD_SIZE)

    def position(self):
        return (round(self.x, 2), round(self.y, 2))

    def __repr__(self):
        return f"UAV {self.id}: ({self.x:.2f}, {self.y:.2f})"


class Artillery:
    def __init__(self):
        self.x = 200
        self.y = 200

    def position(self):
        return (self.x, self.y)