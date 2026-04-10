from sklearn.base import BaseEstimator, TransformerMixin 

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols 
    
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy()
        return X.drop(columns=self.cols, errors="ignore")