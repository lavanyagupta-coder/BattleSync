from sklearn.model_selection import train_test_split

from .config import RANDOM_STATE, TEST_SIZE
from .constants import PREDICTIVE_FEATURES, TARGET_COLUMN


class DataPreprocessor:

    def split(self, dataframe):
        x = dataframe[
            PREDICTIVE_FEATURES
        ].copy()

        y = dataframe[
            TARGET_COLUMN
        ].copy()

        stratify = (
            y
            if y.nunique() > 1
            else None
        )

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=stratify,
        )

        return {
            "x_train": x_train,
            "x_test": x_test,
            "y_train": y_train,
            "y_test": y_test,
        }
