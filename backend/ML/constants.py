TARGET_COLUMN = "Mission_Success"

RAW_PREDICTIVE_FEATURES = [
    "ISR_Delay",
    "Num_Tanks",
    "Num_UAVs",
    "Tank_Speed",
    "Detection_Probability",
]

OUTCOME_COLUMNS = [
    "Destroyed",
    "Survived",
]

ENGINEERED_FEATURES = [
    "UAV_Tank_Ratio",
    "Delay_Per_Tank",
    "Detection_Efficiency",
]

PREDICTIVE_FEATURES = RAW_PREDICTIVE_FEATURES + ENGINEERED_FEATURES

REQUIRED_COLUMNS = (
    RAW_PREDICTIVE_FEATURES
    + OUTCOME_COLUMNS
    + [TARGET_COLUMN]
)

MODEL_NAMES = [
    "Random Forest",
    "Gradient Boosting",
    "XGBoost",
]

METRIC_COLUMNS = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC AUC",
]
