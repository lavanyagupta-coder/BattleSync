import json

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
)

from .config import ENABLE_LIME, ENABLE_SHAP
from .data_loader import DatasetLoader
from .evaluation import Evaluator, ModelComparison
from .explainability import ExplainabilityEngine
from .feature_engineering import FeatureEngineer
from .models import ModelRegistry
from .preprocessing import DataPreprocessor
from .save_model import ModelSaver
from .tuning import HyperParameterTuner


class BattleSyncPipeline:

    def __init__(self):
        self.loader = DatasetLoader()
        self.engineer = FeatureEngineer()
        self.preprocessor = DataPreprocessor()
        self.registry = ModelRegistry()
        self.tuner = HyperParameterTuner()
        self.evaluator = Evaluator()
        self.comparison = ModelComparison()
        self.explainability = ExplainabilityEngine()
        self.saver = ModelSaver()

    def save_plots(
        self,
        model,
        x_test,
        y_test,
        experiment,
        model_name,
    ):
        plots = experiment / "plots"

        ConfusionMatrixDisplay.from_estimator(
            model,
            x_test,
            y_test,
        )

        plt.title(
            f"{model_name} Confusion Matrix"
        )

        plt.tight_layout()

        plt.savefig(
            plots / "confusion_matrix.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        if y_test.nunique() > 1:
            RocCurveDisplay.from_estimator(
                model,
                x_test,
                y_test,
            )

            plt.title(
                f"{model_name} ROC Curve"
            )

            plt.tight_layout()

            plt.savefig(
                plots / "roc_curve.png",
                dpi=300,
                bbox_inches="tight",
            )

            plt.close()

            PrecisionRecallDisplay.from_estimator(
                model,
                x_test,
                y_test,
            )

            plt.title(
                f"{model_name} Precision-Recall Curve"
            )

            plt.tight_layout()

            plt.savefig(
                plots
                / "precision_recall_curve.png",
                dpi=300,
                bbox_inches="tight",
            )

            plt.close()

    def train(self):
        dataframe = self.loader.load()

        transformed = self.engineer.transform(
            dataframe
        )

        split = self.preprocessor.split(
            transformed
        )

        x_train = split["x_train"]
        x_test = split["x_test"]
        y_train = split["y_train"]
        y_test = split["y_test"]

        model_results = []
        trained_models = {}
        tuning_results = {}
        evaluations = {}

        for (
            model_name,
            model,
        ) in self.registry.all().items():

            tuned = self.tuner.tune(
                model_name,
                model,
                x_train,
                y_train,
            )

            evaluation = self.evaluator.evaluate(
                tuned["model"],
                x_test,
                y_test,
            )

            metrics = evaluation[
                "metrics"
            ].copy()

            metrics["Model"] = model_name

            metrics["Training Time"] = (
                tuned["training_time"]
            )

            metrics["CV F1 Score"] = (
                tuned["cv_score"]
            )

            model_results.append(
                metrics
            )

            trained_models[
                model_name
            ] = tuned["model"]

            tuning_results[
                model_name
            ] = tuned

            evaluations[
                model_name
            ] = evaluation

        comparison = (
            self.comparison.compare(
                model_results
            )
        )

        best_name = comparison.iloc[
            0
        ]["Model"]

        best_model = trained_models[
            best_name
        ]

        best_evaluation = evaluations[
            best_name
        ]

        best_tuning = tuning_results[
            best_name
        ]

        experiment = self.saver.save(
            model=best_model,
            model_name=best_name,
            metrics=best_evaluation[
                "metrics"
            ],
            parameters=best_tuning[
                "parameters"
            ],
            comparison=comparison,
            feature_names=x_train.columns,
            dataset_size=len(dataframe),
        )

        self.save_plots(
            best_model,
            x_test,
            y_test,
            experiment,
            best_name,
        )

        importance = (
            self.explainability
            .feature_importance(
                best_model,
                x_train.columns,
            )
        )

        if importance is not None:
            importance.to_csv(
                experiment
                / "feature_importance.csv",
                index=False,
            )

        if ENABLE_SHAP:
            self.explainability.shap_analysis(
                best_model,
                x_test,
                experiment / "plots",
            )

        if ENABLE_LIME:
            self.explainability.lime_analysis(
                best_model,
                x_train,
                x_test,
                experiment / "plots",
            )

        report = self.create_report(
            dataframe,
            x_train,
            x_test,
            comparison,
            best_name,
            best_tuning,
            best_evaluation,
        )

        with open(
            experiment
            / "training_report.md",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(report)

        return {
            "model": best_model,
            "model_name": best_name,
            "comparison": comparison,
            "metrics": best_evaluation[
                "metrics"
            ],
            "parameters": best_tuning[
                "parameters"
            ],
            "output": experiment,
        }

    def create_report(
        self,
        dataframe,
        x_train,
        x_test,
        comparison,
        best_name,
        best_tuning,
        best_evaluation,
    ):
        comparison_markdown = (
            comparison.to_markdown(
                index=False
            )
        )

        parameters = json.dumps(
            best_tuning["parameters"],
            indent=2,
        )

        metrics = json.dumps(
            best_evaluation["metrics"],
            indent=2,
        )

        features = "\n".join(
            f"- {feature}"
            for feature in x_train.columns
        )

        return f"""# BattleSync ML & Analytics Training Report

## Dataset

Rows: {len(dataframe)}

Training samples: {len(x_train)}

Testing samples: {len(x_test)}

{features}
{comparison_markdown}
{best_name}
{parameters}
