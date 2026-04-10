from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd 

class BaseDFTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self 
    
class BinaryEncoder(BaseDFTransformer):
    def __init__(self, mappings):
        self.mappings = mappings 
    
    def transform(self, X):
        X = X.copy()

        for col, mapping in self.mappings.items():
            if col in X.columns:
                X[col] = X[col].map(mapping)
                X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)
        return X 
    
class OrdinalEncoderCustom(BaseDFTransformer):
    def __init__(self, mappings):
        self.mappings = mappings 

    def transform(self, X):
        X = X.copy()

        for col, mapping in self.mappings.items():
            if col in X.columns:
                X[col] = X[col].map(mapping)
                X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

        return X
    
class FoundationEncoder(BaseDFTransformer):
    def __init__(self, mapping, column="Foundation", default_value=0):
        self.mapping = mapping
        self.column = column
        self.default_value = default_value

    def transform(self, X):
        X = X.copy()

        if self.column in X.columns:
            X[self.column] = X[self.column].map(self.mapping).fillna(self.default_value)

        return X