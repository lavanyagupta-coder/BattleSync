import random

from agents import Tank, UAV
from config import (
    DEFAULT_TANKS,
    DEFAULT_UAVS,
    DEFAULT_TANK_SPEED,
    DEFAULT_ISR_DELAY,
    BATTLEFIELD_SIZE,
    STRIKE_RADIUS,
)

from isr import detect
from utils import success_percentage


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


def run_once(
    num_tanks=DEFAULT_TANKS,
    num_uavs=DEFAULT_UAVS,
    tank_speed=DEFAULT_TANK_SPEED,
    isr_delay=DEFAULT_ISR_DELAY,
):

    tanks = [Tank(i + 1) for i in range(num_tanks)]
    uavs = [UAV(i + 1) for i in range(num_uavs)]

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

                delay = isr_delay

                for _ in range(delay):
                    move_tank(tank, tank_speed)

                if artillery_strike(old_x, old_y, tank):
                    tank.alive = False
                    destroyed += 1

                break

        if not detected:
            move_tank(tank, tank_speed)

    survived = num_tanks - destroyed

    return {
        "total_tanks": num_tanks,
        "destroyed": destroyed,
        "survived": survived,
        "success_percentage": success_percentage(destroyed, num_tanks),
    }


if __name__ == "__main__":

    result = run_once()

    print(result)