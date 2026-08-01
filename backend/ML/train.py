from .pipeline import BattleSyncPipeline


def main():
    pipeline = BattleSyncPipeline()

    result = pipeline.train()

    print(
        result["comparison"].to_string(
            index=False
        )
    )

    print(
        f"\nBest Model: {result['model_name']}"
    )

    print(
        f"Output: {result['output']}"
    )


if __name__ == "__main__":
    main()
