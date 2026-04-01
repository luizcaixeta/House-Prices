import numpy as np 
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureCreator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy()

        X['TotalBathrooms'] = (
            X['FullBath']
            + 0.5 * X['HalfBath']
            + X['BsmtFullBath']
            + 0.5 * X['BsmtHalfBath']
        )

        X['Remod'] = (X['YearBuilt'] != X['YearRemodAdd']).astype(int)

        X['Age'] = X['YrSold'] - X['YearRemodAdd']

        return X 
    
class BinarizeFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy()

        X['has_pool'] = X['PoolQC'].isin(['Ex', 'Fa', 'Gd']).astype(int)
        X['has_misc_feature'] = X['MiscFeature'].isin(['Shed', 'Gar2', 'Othr', 'TenC']).astype(int)

        return X
    
    