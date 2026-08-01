from pathlib import Path

import pandas as pd

from .config import MODEL_DIR
from .constants import RAW_PREDICTIVE_FEATURES
from .feature_engineering import FeatureEngineer
from .utils import load_json, load_pickle


class BattlefieldPredictor:

    def __init__(
        self,
        model_directory=None,
    ):
        directory = (
            Path(model_directory)
            if model_directory
            else MODEL_DIR / "latest"
        )

        model_path = (
            directory / "model.pkl"
        )

        metadata_path = (
            directory / "metadata.json"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata not found: {metadata_path}"
            )

        self.model = load_pickle(
            model_path
        )

        self.metadata = load_json(
            metadata_path
        )

        self.feature_engineer = (
            FeatureEngineer()
        )

    def validate(self, data):
        missing = [
            feature
            for feature in RAW_PREDICTIVE_FEATURES
            if feature not in data
        ]

        if missing:
            raise ValueError(
                f"Missing prediction fields: {missing}"
            )

    def predict(self, data):
        self.validate(data)

        dataframe = pd.DataFrame(
            [data]
        )

        dataframe = (
            self.feature_engineer.transform(
                dataframe
            )
        )

        feature_names = self.metadata[
            "feature_names"
        ]

        x = dataframe[
            feature_names
        ]

        prediction = int(
            self.model.predict(x)[0]
        )

        probability = (
            self.model.predict_proba(x)[0]
        )

        confidence = float(
            probability[
                prediction
            ]
        )

        return {
            "prediction": prediction,
            "mission": (
                "Mission Success"
                if prediction == 1
                else "Mission Failure"
            ),
            "confidence": confidence,
            "probability": {
                "failure": float(
                    probability[0]
                ),
                "success": float(
                    probability[1]
                ),
            },
        }
