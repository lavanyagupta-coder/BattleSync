import numpy as np

from .constants import PREDICTIVE_FEATURES


class FeatureEngineer:

    def transform(self, dataframe):
        transformed = dataframe.copy()

        tanks = transformed[
            "Num_Tanks"
        ].replace(0, np.nan)

        transformed["UAV_Tank_Ratio"] = (
            transformed["Num_UAVs"] / tanks
        )

        transformed["Delay_Per_Tank"] = (
            transformed["ISR_Delay"] / tanks
        )

        transformed["Detection_Efficiency"] = (
            transformed["Detection_Probability"]
            * transformed["UAV_Tank_Ratio"]
        )

        transformed.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True,
        )

        transformed[
            PREDICTIVE_FEATURES
        ] = transformed[
            PREDICTIVE_FEATURES
        ].fillna(0)

        return transformed
