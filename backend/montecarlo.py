import pandas as pd
from simulator import run_once


def monte_carlo(num_simulations=10000):

    results = []

    total_destroyed = 0
    total_survived = 0

    print(f"\nRunning {num_simulations} simulations...\n")

    for i in range(num_simulations):

        result = run_once()

        total_destroyed += result["destroyed"]
        total_survived += result["survived"]

        results.append(result)

        if (i + 1) % 1000 == 0:
            print(f"{i+1} simulations completed")

    average_destroyed = total_destroyed / num_simulations
    average_survived = total_survived / num_simulations

    print("\nSimulation Completed")
    print("----------------------")
    print(f"Average Destroyed : {average_destroyed:.2f}")
    print(f"Average Survived  : {average_survived:.2f}")

    return pd.DataFrame(results)


if __name__ == "__main__":

    df = monte_carlo(10000)

    print(df.head())