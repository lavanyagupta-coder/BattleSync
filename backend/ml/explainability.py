from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ExplainabilityEngine:

    def feature_importance(
        self,
        model,
        feature_names,
    ):
        if not hasattr(
            model,
            "feature_importances_",
        ):
            return None

        dataframe = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importance": model.feature_importances_,
            }
        )

        return dataframe.sort_values(
            by="Importance",
            ascending=False,
        ).reset_index(
            drop=True
        )

    def shap_analysis(
        self,
        model,
        x_test,
        output_directory,
    ):
        try:
            import shap

            output_directory = Path(
                output_directory
            )

            sample = x_test.sample(
                min(len(x_test), 500),
                random_state=42,
            )

            explainer = shap.Explainer(
                model,
                sample,
            )

            values = explainer(
                sample
            )

            shap.summary_plot(
                values,
                sample,
                show=False,
            )

            plt.tight_layout()

            plt.savefig(
                output_directory
                / "shap_summary.png",
                dpi=300,
                bbox_inches="tight",
            )

            plt.close()

            shap.summary_plot(
                values,
                sample,
                plot_type="bar",
                show=False,
            )

            plt.tight_layout()

            plt.savefig(
                output_directory
                / "shap_bar.png",
                dpi=300,
                bbox_inches="tight",
            )

            plt.close()

            raw_values = np.asarray(
                values.values
            )

            if raw_values.ndim == 3:
                raw_values = raw_values[
                    :, :, -1
                ]

            importance = np.abs(
                raw_values
            ).mean(axis=0)

            ranking = pd.DataFrame(
                {
                    "Feature": sample.columns,
                    "Mean_Absolute_SHAP": importance,
                }
            )

            ranking = ranking.sort_values(
                by="Mean_Absolute_SHAP",
                ascending=False,
            )

            ranking.to_csv(
                output_directory
                / "shap_feature_ranking.csv",
                index=False,
            )

            return ranking

        except Exception as error:
            return {
                "error": str(error)
            }

    def lime_analysis(
        self,
        model,
        x_train,
        x_test,
        output_directory,
    ):
        try:
            from lime.lime_tabular import (
                LimeTabularExplainer,
            )

            output_directory = Path(
                output_directory
            )

            explainer = LimeTabularExplainer(
                training_data=x_train.values,
                feature_names=list(
                    x_train.columns
                ),
                class_names=[
                    "Mission Failure",
                    "Mission Success",
                ],
                mode="classification",
                random_state=42,
            )

            explanation = explainer.explain_instance(
                x_test.iloc[0].values,
                model.predict_proba,
                num_features=len(
                    x_train.columns
                ),
            )

            explanation.save_to_file(
                str(
                    output_directory
                    / "lime_explanation.html"
                )
            )

            return explanation.as_list()

        except Exception as error:
            return {
                "error": str(error)
            }
