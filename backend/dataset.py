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

        destroyed_ratio = (
            result["destroyed"] / result["total_tanks"]
            if result["total_tanks"] > 0
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
                "Destroyed_Ratio": destroyed_ratio,
            }
        )

        if (i + 1) % 1000 == 0:
            print(f"{i + 1} records generated")

    df = pd.DataFrame(rows)

    # Label success relative to the dataset's own median destruction ratio.
    # A fixed high threshold (e.g. 70%) can be effectively unreachable given
    # detection coverage limits, which collapses the target to a single
    # class and breaks training. Using the median guarantees a meaningful,
    # roughly balanced split between "above average" and "below average"
    # mission outcomes.
    median_ratio = df["Destroyed_Ratio"].median()

    df["Mission_Success"] = (
        df["Destroyed_Ratio"] >= median_ratio
    ).astype(int)

    df = df.drop(columns=["Destroyed_Ratio"])

    # Create datasets directory automatically
    os.makedirs("../datasets", exist_ok=True)

    df.to_csv("../datasets/battlefield_dataset.csv", index=False)

    print("\nDataset Saved Successfully!")
    print(f"Median destroyed ratio used as success threshold: {median_ratio:.4f}")
    print(f"Class balance -> Success: {(df['Mission_Success']==1).sum()}, "
          f"Failure: {(df['Mission_Success']==0).sum()}")

    return df


if __name__ == "__main__":
    generate_dataset(10000)