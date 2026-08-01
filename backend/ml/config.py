from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

DATASET_DIR = PROJECT_ROOT / "datasets"
DATASET_PATH = DATASET_DIR / "battlefield_dataset.csv"

MODEL_DIR = BACKEND_DIR / "models"
OUTPUT_DIR = BACKEND_DIR / "outputs"
EXPERIMENT_DIR = OUTPUT_DIR / "experiments"

TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5
N_JOBS = -1
RANDOM_SEARCH_ITERATIONS = 20
SCORING_METRIC = "f1"

ENABLE_SHAP = True
ENABLE_LIME = True
