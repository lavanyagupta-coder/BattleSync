from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from xgboost import XGBClassifier

from .config import RANDOM_STATE


class ModelRegistry:

    def __init__(self):
        self.models = {
            "Random Forest": RandomForestClassifier(
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                random_state=RANDOM_STATE,
            ),
            "XGBoost": XGBClassifier(
                objective="binary:logistic",
                eval_metric="logloss",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        }

    def all(self):
        return self.models.copy()

    def get(self, name):
        return self.models[name]

    def names(self):
        return list(
            self.models.keys()
        )
