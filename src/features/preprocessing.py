import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder

class NoneLikeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, fill_value='None'):
        self.columns = tuple(columns)
        self.fill_value = fill_value 

    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy() 

        for col in self.columns:
            if col in X.columns:
                X[col] = X[col].fillna(self.fill_value)
        
        return X
    
class NeighborhoodModeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, neighborhood_col="Neighborhood", fallback_value="Other"):
        self.columns = tuple(columns)
        self.neighborhood_col = neighborhood_col
        self.fallback_value = fallback_value

    def fit(self, X, y=None):
        self.global_modes_ = {}
        self.neighborhood_modes_ = {}

        for col in self.columns:
            if col not in X.columns:
                continue

            global_mode = X[col].mode(dropna=True)
            self.global_modes_[col] = (
                global_mode.iloc[0] if not global_mode.empty else self.fallback_value
            )

            col_modes = (
                X.groupby(self.neighborhood_col)[col]
                .agg(lambda s: s.mode(dropna=True).iloc[0] if not s.mode(dropna=True).empty else self.global_modes_[col])
                .to_dict()
            )

            self.neighborhood_modes_[col] = col_modes

        return self

    def transform(self, X):
        X = X.copy()

        for col in self.columns:
            if col not in X.columns:
                continue

            missing_mask = X[col].isna()

            if missing_mask.any():
                X.loc[missing_mask, col] = (
                    X.loc[missing_mask, self.neighborhood_col]
                    .map(self.neighborhood_modes_.get(col, {}))
                )

            X[col] = X[col].fillna(self.global_modes_.get(col, self.fallback_value))
            X[col] = X[col].fillna(self.fallback_value)

        return X

class RareCategoryGrouper(BaseEstimator, TransformerMixin):
    def __init__(
            self, 
            columns,
            min_freq=0.01,
            other_label='Other',
    ):
        self.columns = tuple(columns)
        self.min_freq = min_freq
        self.other_label = other_label
    
    def fit(self, X, y=None):
        self.frequent_categories_ = {}

        for col in self.columns:
            if col not in X.columns:
                continue

            freq = X[col].fillna(self.other_label).value_counts(normalize=True)
            keep = set(freq[freq >= self.min_freq].index)
            keep.add(self.other_label)

            self.frequent_categories_[col] = keep
        
        return self 
    
    def transform(self, X):
        X = X.copy()

        for col, keep in self.frequent_categories_.items():
            if col in X.columns:
                X[col] = X[col].fillna(self.other_label)
                X[col] = X[col].where(X[col].isin(keep), self.other_label)
        
        return X 
    
class ColumnValueMapper(BaseEstimator, TransformerMixin):
    def __init__(self, column, mapping, default_value="Other"):
        self.column = column
        self.mapping = mapping
        self.default_value = default_value

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        if self.column in X.columns:
            X[self.column] = X[self.column].map(self.mapping).fillna(self.default_value)

        return X
    
class SafeOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, other_label="Other"):
        self.columns = columns
        self.other_label = other_label

    def fit(self, X, y=None):
        X = X.copy()

        if self.columns is None:
            self.columns_ = list(X.select_dtypes(include=["object", "category"]).columns)
        else:
            self.columns_ = [col for col in self.columns if col in X.columns]

        self.non_encoded_cols_ = [col for col in X.columns if col not in self.columns_]

        if not self.columns_:
            self.encoder_ = None
            return self

        self.allowed_categories_ = {}
        categories = []

        for col in self.columns_:
            values = X[col].astype(object).fillna(self.other_label)
            unique_values = list(pd.Index(values.unique()))

            if self.other_label not in unique_values:
                unique_values.append(self.other_label)

            self.allowed_categories_[col] = set(unique_values)
            categories.append(unique_values)

        self.encoder_ = OneHotEncoder(
            categories=categories,
            handle_unknown="ignore",
            sparse_output=False,
        )

        X_prepared = self._prepare_input(X)
        self.encoder_.fit(X_prepared[self.columns_])
        self.feature_names_out_ = self.encoder_.get_feature_names_out(self.columns_)

        return self

    def _prepare_input(self, X):
        X = X.copy()

        for col in self.columns_:
            X[col] = X[col].astype(object).fillna(self.other_label)
            X[col] = X[col].where(
                X[col].isin(self.allowed_categories_[col]),
                self.other_label
            )

        return X

    def transform(self, X):
        X = X.copy()

        if self.encoder_ is None:
            return X

        X_prepared = self._prepare_input(X)

        encoded = self.encoder_.transform(X_prepared[self.columns_])
        encoded_df = pd.DataFrame(
            encoded,
            columns=self.feature_names_out_,
            index=X_prepared.index,
        )

        return pd.concat(
            [X_prepared[self.non_encoded_cols_], encoded_df],
            axis=1
        )

class NumericZeroImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        num_cols = X.select_dtypes(include=["number"]).columns
        X[num_cols] = X[num_cols].fillna(0)

        return X

class CategoricalMissingImputer(BaseEstimator, TransformerMixin):
    def __init__(self, fill_value='Missing'):
        self.fill_value = fill_value 

    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy()

        cat_cols = X.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            X[col] = X[col].fillna(self.fill_value)

        return X