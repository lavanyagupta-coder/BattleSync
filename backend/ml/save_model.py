import shutil

from .config import MODEL_DIR
from .utils import (
    create_experiment_directory,
    save_json,
    save_pickle,
)


class ModelSaver:

    def save(
        self,
        model,
        model_name,
        metrics,
        parameters,
        comparison,
        feature_names,
        dataset_size,
    ):
        experiment = create_experiment_directory()

        save_pickle(model, experiment / "model.pkl")

        metadata = {
            "model_name": model_name,
            "feature_names": list(feature_names),
            "metrics": metrics,
            "parameters": parameters,
            "dataset_size": dataset_size,
        }

        save_json(metadata, experiment / "metadata.json")

        comparison.to_csv(
            experiment / "model_comparison.csv",
            index=False,
        )

        self._update_latest(experiment)

        return experiment

    def _update_latest(self, experiment):
        latest = MODEL_DIR / "latest"

        if latest.is_symlink() or latest.is_file():
            latest.unlink()
        elif latest.exists():
            shutil.rmtree(latest)

        try:
            latest.symlink_to(experiment, target_is_directory=True)
        except OSError:
            # Windows without symlink permission — fall back to a copy
            shutil.copytree(experiment, latest)