import time

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


class Evaluator:

    def evaluate(
        self,
        model,
        x_test,
        y_test,
    ):
        start = time.perf_counter()

        predictions = model.predict(
            x_test
        )

        prediction_time = (
            time.perf_counter() - start
        )

        probabilities = None
        roc_auc = None

        if hasattr(
            model,
            "predict_proba",
        ):
            probabilities = model.predict_proba(
                x_test
            )[:, 1]

            if y_test.nunique() > 1:
                roc_auc = roc_auc_score(
                    y_test,
                    probabilities,
                )

        metrics = {
            "Accuracy": float(
                accuracy_score(
                    y_test,
                    predictions,
                )
            ),
            "Precision": float(
                precision_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            "Recall": float(
                recall_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            "F1 Score": float(
                f1_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            "ROC AUC": (
                float(roc_auc)
                if roc_auc is not None
                else None
            ),
            "Prediction Time": float(
                prediction_time
            ),
        }

        return {
            "metrics": metrics,
            "predictions": predictions,
            "probabilities": probabilities,
            "confusion_matrix": confusion_matrix(
                y_test,
                predictions,
            ),
            "classification_report": classification_report(
                y_test,
                predictions,
                output_dict=True,
                zero_division=0,
            ),
        }


class ModelComparison:

    def compare(self, results):
        dataframe = pd.DataFrame(
            results
        )

        return dataframe.sort_values(
            by="F1 Score",
            ascending=False,
        ).reset_index(
            drop=True
        )
