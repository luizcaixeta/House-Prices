import numpy as np 
import pandas as pd 

def data_cleaning(df):
    none_cols = [
        "PoolQC", "MiscFeature", "Alley", "Fence", 
        "MasVnrType", "FireplaceQu", "GarageType", "GarageFinish",
        "GarageQual", "BsmtFinType2", "BsmtQual", "BsmtQual", 
        "BsmtCond", "BsmtFinType1", "BsmtFinType2", "BsmtExposure", 
        "GarageCond"
    ]

    for col in none_cols:
        df[col] = df[col].fillna("None")

    df["LotFrontage"] = df.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(df["YearBuilt"])
    df["MasVnrType"] = df["MasVnrArea"].fillna(0)
    df["MasVnrArea"] = df["MasVnrArea"].fillna(0)
    df["Electrical"] = df["Electrical"].fillna(df["Electrical"].mode()[0])

    return df 

def ordinal_variables(qual_map, ordinal_cols, df):

    for col in ordinal_cols:
        df[col] = df[col].map(qual_map)

    df[ordinal_cols] = df[ordinal_cols].fillna(0).astype(float)
    
    return df