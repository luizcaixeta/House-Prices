from sklearn.pipeline import Pipeline
from src.config.feature_engineering_config import (
    TARGET_COL,
    NONE_LIKE_COLUMNS,
    OTHER_LABEL,
    DEFAULT_DROP_COLUMNS,
    RARE_GROUP_COLUMNS,
    NEIGHBORHOOD_MODE_COLUMNS,
    POOL_CATEGORIES,
    MISC_FEATURE_CATEGORIES,
    BINARY_MAPPINGS,
    ORDINAL_MAPPINGS,
    FOUNDATION_GROUP_MAPPING,
)
from src.features.preprocessing import (
    NoneLikeImputer,
    NeighborhoodModeImputer,
    RareCategoryGrouper,
    ColumnValueMapper,
    SafeOneHotEncoder,
    NumericZeroImputer,
)
from src.features.encoders import BinaryEncoder, OrdinalEncoderCustom
from src.features.creators import FeatureCreator, BinarizeFeatures
from src.features.aggregations import NeighborhoodScore
from src.features.selectors import ColumnDropper

def build_pipeline(rare_min_freq: float = 0.01):
    none_like_cols = tuple(
        col for col in NONE_LIKE_COLUMNS
        if col not in NEIGHBORHOOD_MODE_COLUMNS
    )

    drop_cols = tuple(dict.fromkeys(DEFAULT_DROP_COLUMNS))

    pipeline = Pipeline([
        (
            "neighborhood_mode_imputer",
            NeighborhoodModeImputer(
                columns=NEIGHBORHOOD_MODE_COLUMNS,
                neighborhood_col="Neighborhood",
                fallback_value=OTHER_LABEL,
            ),
        ),
        (
            "none_like_imputer",
            NoneLikeImputer(
                columns=none_like_cols,
                fill_value="None",
            ),
        ),
        (
            "rare_grouper",
            RareCategoryGrouper(
                columns=RARE_GROUP_COLUMNS,
                min_freq=rare_min_freq,
                other_label=OTHER_LABEL,
            ),
        ),
        (
            "foundation_mapper",
            ColumnValueMapper(
                column="Foundation",
                mapping=FOUNDATION_GROUP_MAPPING,
                default_value=OTHER_LABEL,
            ),
        ),
        ("binary", BinaryEncoder(BINARY_MAPPINGS)),
        ("ordinal", OrdinalEncoderCustom(ORDINAL_MAPPINGS)),
        ("features", FeatureCreator()),
        (
            "binarize",
            BinarizeFeatures(
                pool_categories=POOL_CATEGORIES,
                misc_feature_categories=MISC_FEATURE_CATEGORIES,
            ),
        ),
        (
            "neighborhood_score",
            NeighborhoodScore(
                target_col=TARGET_COL,
                output_col="NeighborhoodScore",
            ),
        ),
        ("drop", ColumnDropper(drop_cols)),
        (
            "onehot",
            SafeOneHotEncoder(other_label=OTHER_LABEL),
        ),
        ("num_zero", NumericZeroImputer()),
    ])

    return pipeline