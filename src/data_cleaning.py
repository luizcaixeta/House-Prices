import numpy as np 
import pandas as pd 

def data_cleaning(df):

    df_clean = df.copy()

    # substituir missing por "None" nas variáveis categóricas que indicam ausência da característica
    columns_none = [
        'PoolQC', 'MiscFeature', 'Alley', 'Fence', 'MasVnrType',
        'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual',
        'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'BsmtQual', 'BsmtCond',
        'GarageCond'
    ]

    for col in columns_none:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('None')

    # LotFrontage: imputar pela mediana do bairro (Neighborhood)
    if 'LotFrontage' in df_clean.columns and 'Neighborhood' in df_clean.columns:
        df_clean['LotFrontage'] = df_clean.groupby('Neighborhood')['LotFrontage'].transform(
            lambda x: x.fillna(x.median())
        )

    # GarageYrBlt: preencher faltantes com YearBuilt (ano de construção da casa)
    if 'GarageYrBlt' in df_clean.columns and 'YearBuilt' in df_clean.columns:
        df_clean['GarageYrBlt'] = df_clean['GarageYrBlt'].fillna(df_clean['YearBuilt'])

    # MasVnrArea: definir como 0 se MasVnrType for 'None'
    if 'MasVnrArea' in df_clean.columns and 'MasVnrType' in df_clean.columns:
        # Se MasVnrType for 'None' (ou NaN), MasVnrArea deve ser 0
        df_clean['MasVnrArea'] = df_clean.apply(
            lambda row: 0 if row['MasVnrType'] == 'None' else row['MasVnrArea'],
            axis=1
        )

        df_clean['MasVnrArea'] = df_clean['MasVnrArea'].fillna(0)

    # Electrical: preencher pela moda
    if 'Electrical' in df_clean.columns:
        mode_electrical = df_clean['Electrical'].mode()[0]
        df_clean['Electrical'] = df_clean['Electrical'].fillna(mode_electrical)

    return df_clean