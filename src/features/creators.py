from sklearn.base import BaseEstimator, TransformerMixin

class FeatureCreator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X["TotalBathrooms"] = (
            X["FullBath"]
            + 0.5 * X["HalfBath"]
            + X["BsmtFullBath"]
            + 0.5 * X["BsmtHalfBath"]
        )

        X["Remod"] = (X["YearBuilt"] != X["YearRemodAdd"]).astype(int)
        X["Age"] = X["YrSold"] - X["YearRemodAdd"]

        return X


class BinarizeFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, pool_categories, misc_feature_categories):
        self.pool_categories = tuple(pool_categories)
        self.misc_feature_categories = tuple(misc_feature_categories)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X["has_pool"] = X["PoolQC"].isin(self.pool_categories).astype(int)
        X["has_misc_feature"] = X["MiscFeature"].isin(self.misc_feature_categories).astype(int)

        return X