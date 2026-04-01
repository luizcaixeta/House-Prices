import pandas as pd 
import numpy as np 
from features.feature_engineering_config import BINARY_MAPPINGS, ORDINAL_MAPPINGS

def sale_price(df: pd.DataFrame) -> pd.DataFrame:
    df['SalePrice'] = np.log1p(df['Saleprice'])

    return df 

def encode_binary(df: pd.DataFrame) -> pd.DataFrame:

    for col, mapping in BINARY_MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    return df
    
def encode_ordinal(df: pd.DataFrame) -> pd.DataFrame:

    for col, mapping in ORDINAL_MAPPINGS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)
    
    return df 

def compute_neighborhood_score(df: pd.DataFrame) -> pd.DataFrame:

    neigh = df.groupby('Neighborhood').agg({
        'SalePrice': 'mean',
        'OverallQual': 'mean',
        'YearBuilt': 'mean'
    })

    neigh = neigh.rename(columns={
        'OverallQual': 'Qual_mean'
    })

    for col in ['SalePrice', 'Qual_mean', 'YearBuilt']:
        neigh[col + "_z"] = (neigh[col] - neigh[col].mean()) / neigh[col].std()

    neigh['Score'] = (
        0.5 * neigh['SalePrice_z'] + 
        0.3 * neigh['Qual_mean_z'] +
        0.2 * neigh['YearBuilt_z']
    )

    df = df.copy()
    df['Neighborhood'] = df['Neighborhood'].map(neigh['Score'])

    return df 

def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns= [
        'Utilities',
        'EnclosedPorch',
        '3SsnPorch',
        'ScreenPorch',
        'KitchenQual',
        'TotRmsAbvGrd',
        'GarageYrBlt',
        'GarageArea',
        '1stFlrSF',
        '2ndFlrSF',
        'PoolArea',
        'MoSold'
    ])

    return df 

def group_rare_auto(df, cols, threshold):

    df = df.copy()

    for col in cols:
        freq = df[col].value_counts(normalize=True)
        rare = freq[freq < threshold].index 

        df[col] = df[col].replace(rare, 'Other')

    return df 

def total_bathrooms(df: pd.DataFrame) -> pd.DataFrame:
    df['TotalBathrooms'] = (
        df['FullBath']
        + 0.5 * df['HalfBath']
        + df['BsmtFullBath'] 
        + 0.5 * df['BsmtHalfBath']
    )

    df.drop(columns=['FullBath', 'HalfBath', 'BsmtFullBath', 'BsmtHalfBath'])

    return df 

def remod(df: pd.DataFrame) -> pd.DataFrame:

    df['Remod'] = np.where(df['YearBuilt'] == df['YearRemodAdd'], 0, 1)
    return df 

def age(df: pd.DataFrame) -> pd.DataFrame:

    df['Age'] = df['YrSold'] - df['YearRemodAdd']

    df.drop(columns=['YrSold', 'YearRemodAdd'])

    return df 

def binarize_poolqc(df, col_name='PoolQC', new_col_name='has_pool'):

    pool_categories = ['Ex', 'Fa', 'Gd']
    
    df[new_col_name] = df[col_name].apply(
        lambda x: 1 if x in pool_categories else 0
    )
    df[new_col_name] = df[new_col_name].fillna(0).astype(int)
    
    return df

def binarize_miscfeature(df, col_name='MiscFeature', new_col_name='has_misc_feature'):

    misc_feature_categories = ['Shed', 'Gar2', 'Othr', 'TenC']
    
    df[new_col_name] = df[col_name].apply(
        lambda x: 1 if x in misc_feature_categories else 0
    )
    df[new_col_name] = df[new_col_name].fillna(0).astype(int)
    
    return df

def encode_foundation(df: pd.DataFrame) -> pd.DataFrame:

    mapping_foundation = {'BrkTil': 1, 'CBlock': 2, 'PConc': 3}
    df['Foundation'] = df['Foundation'].map(mapping_foundation).fillna(0).astype(int)
    return df
