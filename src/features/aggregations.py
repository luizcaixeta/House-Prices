import pandas as pd 
from sklearn.base import BaseEstimator, TransformerMixin

class NeighborhoodScore(BaseEstimator, TransformerMixin):
    def __init__(
            self, 
            neighborhood_col: str = "Neighborhood",
            target_col: str = "SalePrice",
            output_col: str = "NeighborhoodScore",
            fill_value: float = 0.0,
    ):
        self.neighborhood_col = neighborhood_col
        self.target_col = target_col
        self.output_col = output_col
        self.fill_value = fill_value

    def _zscore(self, series: pd.Series) -> pd.Series:
        std = series.std() 

        if std == 0 or pd.isna(std):
            return pd.Series(0.0, index=series.index)
        return (series - series.mean()) / std 
    
    def fit(self, X, y):
        
        required_cols = [self.neighborhood_col, "OverallQual", "YearBuilt"]
        missing_cols = [col for col in required_cols if col not in X.columns]
        if missing_cols:
            raise ValueError(
                f"Colunas ausentes para NeighborhoodScore: {missing_cols}"
            )
        
        df = X[required_cols].copy()
        df[self.target_col] = pd.Series(y, index=X.index)

        neigh = df.groupby(self.neighborhood_col).agg(
            SalePrice=(self.target_col, "mean"),
            Qual_mean=("OverallQual", "mean"),
            YearBuilt=("YearBuilt", "mean"),
        )

        neigh["SalePrice_z"] = self._zscore(neigh["SalePrice"])
        neigh["Qual_mean_z"] = self._zscore(neigh["Qual_mean"])
        neigh["YearBuilt_z"] = self._zscore(neigh["YearBuilt"])

        neigh["Score"] = (
            0.5 * neigh["SalePrice_z"] 
            + 0.3 * neigh["Qual_mean_z"]
            + 0.2 * neigh["YearBuilt_z"]
        )

        self.mapping_ = neigh["Score"].to_dict()
        self.default_score_= (
            float(neigh["Score"].mean()) if not neigh.empty else self.fill_value 
        )

        return self 
    
    def transform(self, X):
        X = X.copy()

        X[self.output_col] = (
            X[self.neighborhood_col].map(self.mapping_).fillna(self.default_score_)
        )

        return X
