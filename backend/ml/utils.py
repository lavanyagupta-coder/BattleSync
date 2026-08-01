from datetime import datetime
from pathlib import Path
import json

import joblib

from .config import EXPERIMENT_DIR, MODEL_DIR, OUTPUT_DIR


def create_directories():
    for directory in [
        MODEL_DIR,
        OUTPUT_DIR,
        EXPERIMENT_DIR,
    ]:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )


def create_experiment_directory():
    create_directories()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    directory = EXPERIMENT_DIR / timestamp

    directory.mkdir(
        parents=True,
        exist_ok=False,
    )

    (directory / "plots").mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def save_json(data, path):
    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            default=str,
        )


def load_json(path):
    with open(
        path,
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_pickle(obj, path):
    joblib.dump(
        obj,
        path,
    )


def load_pickle(path):
    return joblib.load(path)
