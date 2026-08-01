import time

from sklearn.model_selection import RandomizedSearchCV

from .config import (
    CV_FOLDS,
    N_JOBS,
    RANDOM_SEARCH_ITERATIONS,
    RANDOM_STATE,
    SCORING_METRIC,
)


PARAMETER_DISTRIBUTIONS = {
    "Random Forest": {
        "n_estimators": [
            100,
            200,
            300,
            500,
        ],
        "max_depth": [
            None,
            5,
            10,
            20,
        ],
        "min_samples_split": [
            2,
            5,
            10,
        ],
        "min_samples_leaf": [
            1,
            2,
            4,
        ],
    },
    "Gradient Boosting": {
        "n_estimators": [
            100,
            200,
            300,
        ],
        "learning_rate": [
            0.01,
            0.05,
            0.1,
            0.2,
        ],
        "max_depth": [
            2,
            3,
            5,
        ],
        "subsample": [
            0.8,
            1.0,
        ],
    },
    "XGBoost": {
        "n_estimators": [
            100,
            200,
            300,
        ],
        "max_depth": [
            3,
            5,
            7,
        ],
        "learning_rate": [
            0.01,
            0.05,
            0.1,
            0.2,
        ],
        "subsample": [
            0.8,
            1.0,
        ],
        "colsample_bytree": [
            0.8,
            1.0,
        ],
    },
}


class HyperParameterTuner:

    def tune(
        self,
        model_name,
        model,
        x_train,
        y_train,
    ):
        if y_train.nunique() < 2:
            raise ValueError(
                "Training target contains only one class."
            )

        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=PARAMETER_DISTRIBUTIONS[
                model_name
            ],
            n_iter=RANDOM_SEARCH_ITERATIONS,
            scoring=SCORING_METRIC,
            cv=CV_FOLDS,
            random_state=RANDOM_STATE,
            n_jobs=N_JOBS,
            refit=True,
        )

        start = time.perf_counter()

        search.fit(
            x_train,
            y_train,
        )

        training_time = (
            time.perf_counter() - start
        )

        return {
            "model": search.best_estimator_,
            "cv_score": float(
                search.best_score_
            ),
            "parameters": search.best_params_,
            "training_time": training_time,
        }
