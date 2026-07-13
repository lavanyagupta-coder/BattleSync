import random

from agents import Tank, UAV
from config import (
    DEFAULT_TANKS,
    DEFAULT_UAVS,
    BATTLEFIELD_SIZE,
    TANK_SPEED,
    MAX_ISR_DELAY,
    STRIKE_RADIUS,
)

from isr import detect


def move_tank(tank, speed):
    """
    Move tank randomly.
    """

    dx = random.uniform(-speed, speed)
    dy = random.uniform(-speed, speed)

    tank.x += dx
    tank.y += dy

    tank.x = max(0, min(BATTLEFIELD_SIZE, tank.x))
    tank.y = max(0, min(BATTLEFIELD_SIZE, tank.y))


def artillery_strike(old_x, old_y, tank):
    """
    Strike succeeds if tank hasn't moved too far from
    detected position.
    """

    distance = ((old_x - tank.x) ** 2 + (old_y - tank.y) ** 2) ** 0.5

    if distance <= STRIKE_RADIUS:
        return True

    return False


def run_once():

    tanks = [Tank(i + 1) for i in range(DEFAULT_TANKS)]
    uavs = [UAV(i + 1) for i in range(DEFAULT_UAVS)]

    destroyed = 0

    for tank in tanks:

        if not tank.alive:
            continue

        detected = False

        for uav in uavs:

            if detect(uav, tank):
                detected = True

                old_x = tank.x
                old_y = tank.y

                # ISR Delay
                delay = random.randint(0, MAX_ISR_DELAY)

                # Tank moves while ISR info reaches artillery
                for _ in range(delay):
                    move_tank(tank, TANK_SPEED)

                # Artillery attacks old location
                if artillery_strike(old_x, old_y, tank):
                    tank.alive = False
                    destroyed += 1

                break

        if not detected:
            move_tank(tank, TANK_SPEED)

    return {
        "total_tanks": DEFAULT_TANKS,
        "destroyed": destroyed,
        "survived": DEFAULT_TANKS - destroyed,
    }


if __name__ == "__main__":

    result = run_once()

    print(result)