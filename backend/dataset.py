import os
import random
import pandas as pd

from simulator import run_once


def generate_dataset(records=10000):

    rows = []

    print("Generating Dataset...\n")

    for i in range(records):

        delay = random.randint(0, 20)

        tanks = random.randint(10, 50)

        uavs = random.randint(2, 8)

        tank_speed = random.randint(1, 6)

        detection_probability = round(random.uniform(0.6, 1.0), 2)

        # Run simulation using generated parameters
        result = run_once(
            num_tanks=tanks,
            num_uavs=uavs,
            tank_speed=tank_speed,
            isr_delay=delay,
        )

        mission_success = (
            1
            if result["destroyed"] >= result["total_tanks"] * 0.70
            else 0
        )

        rows.append(
            {
                "ISR_Delay": delay,
                "Num_Tanks": tanks,
                "Num_UAVs": uavs,
                "Tank_Speed": tank_speed,
                "Detection_Probability": detection_probability,
                "Destroyed": result["destroyed"],
                "Survived": result["survived"],
                "Mission_Success": mission_success,
            }
        )

        if (i + 1) % 1000 == 0:
            print(f"{i + 1} records generated")

    df = pd.DataFrame(rows)

    # Create datasets directory automatically
    os.makedirs("../datasets", exist_ok=True)

    df.to_csv("../datasets/battlefield_dataset.csv", index=False)

    print("\nDataset Saved Successfully!")

    return df


if __name__ == "__main__":
    generate_dataset(10000)