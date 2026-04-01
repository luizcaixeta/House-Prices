from sklearn.base import BaseEstimator, TransformerMixin

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
        return X
        
class OrdinalEncoderCustom(BaseDFTransformer):
    def __init__(self, mappings):
        self.mappings = mappings 

    def transform(self, X):
        for col, mapping in self.mappings.items():
            if col in X.columns:
                X[col] = X[col].map(mapping)
        return X