from pathlib import Path

import pandas as pd

from .config import DATASET_PATH
from .constants import REQUIRED_COLUMNS, TARGET_COLUMN


class DatasetLoader:

    def __init__(self, dataset_path=DATASET_PATH):
        self.dataset_path = Path(dataset_path)

    def validate(self, dataframe):
        if dataframe.empty:
            raise ValueError(
                "Dataset is empty."
            )

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        if dataframe[TARGET_COLUMN].isna().any():
            raise ValueError(
                "Target column contains missing values."
            )

        unique_targets = set(
            dataframe[TARGET_COLUMN].unique()
        )

        if not unique_targets.issubset({0, 1}):
            raise ValueError(
                "Mission_Success must contain only 0 and 1."
            )

    def load(self):
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        dataframe = pd.read_csv(
            self.dataset_path
        )

        self.validate(dataframe)

        return dataframe
