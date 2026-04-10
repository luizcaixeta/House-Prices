TARGET_COL = 'SalePrice'
ID_COL = 'Id'
OTHER_LABEL = 'Other'
MISSING_LABEL = 'Missing'

NONE_LIKE_COLUMNS = (
    'PoolQC',
    'MiscFeature',
    'Alley',
    'Fence',
    'MasVnrType',
    'FireplaceQu',
    'GarageType',
    'GarageFinish',
    'GarageQual',
    'BsmtExposure',
    'BsmtFinType1',
    'BsmtFinType2',
    'BsmtQual',
    'BsmtCond',
    'GarageCond'
)

DEFAULT_DROP_COLUMNS = (
    ID_COL,
    'Utilities',
    'FullBath',
    'HalfBath',
    'BsmtFullBath',
    'BsmtHalfBath',
    'YrSold',
    'YearRemodAdd',
    'EnclosedPorch',
    '3SsnPorch',
    'ScreenPorch',
    'KitchenQual',
    'RmsAbvGrd',
    'GarageYrBlt',
    'GarageArea',
    '1stFlrSF',
    '2ndFlrSF',
    'PoolArea',
    'MoSold',
    'Neighborhood',
    'Exterior1st',
    'Exterior2nd',
)

DEFAULT_RARE_COLUMNS = (
    'Electrical',
    'Exterior1st',
    'Exterior2nd',
    'Heating',
    'LotConfig',
    'MSZoning',
    'RoofMatl',
    'RoofStyle',
    'SaleCondition',
    'SaleType',
    'HouseStyle'
)

POOL_CATEGORIES = (
    'Ex',
    'Fa',
    'Gd'
)

MISC_FEATURE_CATEGORIES = (
    'Shed',
    'Gar2',
    'Othr',
    'TenC'
)

BINARY_MAPPINGS = {
    'CentralAir': {'N': 0, 'Y': 1},
    'Street': {'Grvl': 0, 'Pave': 1}
}

ORDINAL_MAPPINGS = { 
    'ExterQual': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'ExterCond': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'BsmtQual': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'BsmtCond': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'KitchenQual': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'FireplaceQu': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'GarageQual': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'GarageCond': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'HeatingQC': {'None': 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5},
    'BsmtExposure': {'None': 0, 'No': 1, 'Mn': 2, 'Av': 3, 'Gd': 4},
    'BsmtFinType1': {
        'None': 0,
        'Unf': 1,
        'LwQ': 2,
        'Rec': 3,
        'BLQ': 4,
        'ALQ': 5,
        'GLQ': 6,
    },
    'BsmtFinType2': {
        'None': 0,
        'Unf': 1,
        'LwQ': 2,
        'Rec': 3,
        'BLQ': 4,
        'ALQ': 5,
        'GLQ': 6,
    },
    'Functional': {
        'Sal': 0,
        'Sev': 1,
        'Maj2': 2,
        'Maj1': 3,
        'Mod': 4,
        'Min2': 5,
        'Min1': 6,
        'Typ': 7,
    },
    'GarageFinish': {'None': 0, 'Unf': 1, 'RFn': 2, 'Fin': 3},
    'Fence': {'None': 0, 'MnWw': 1, 'GdWo': 2, 'MnPrv': 3, 'GdPrv': 4},
    'LotShape': {'IR3': 0, 'IR2': 1, 'IR1': 2, 'Reg': 3},
    'LandSlope': {'Sev': 0, 'Mod': 1, 'Gtl': 2},
    'Alley': {'None': 0, 'Grvl': 1, 'Pave': 2},
    'MasVnrType': {'BrkCmnn': 0, 'None': 1, 'BrkFace': 2, 'Stone': 3},
}

NEIGHBORHOOD_MODE_COLUMNS = (
    'MSZoning',
    'Electrical',
    'Heating',
    'LotConfig',
    'MiscFeature',
    'RoofMatl',
    'RoofStyle',
    'SaleCondition',
    'SaleType',
)

RARE_GROUP_COLUMNS = NEIGHBORHOOD_MODE_COLUMNS

FOUNDATION_GROUP_MAPPING = {
    'BrkTil': 'BrkTil',
    'CBlock': 'CBlock',
    'PConc': 'PConc',
}