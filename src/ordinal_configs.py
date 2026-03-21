ordinal_configs = [
    {
        "map": { "Po":1, "Fa":2, "TA":3, "Gd":4, "Ex":5 },
        "cols": ["ExterQual","ExterCond","BsmtQual","BsmtCond",
                 "KitchenQual","FireplaceQu","GarageQual",
                 "GarageCond","PoolQC","HeatingQC"]
    },
    {
        "map": {"No":0,"Mn":1,"Av":2,"Gd":3},
        "cols": ["BsmtExposure"]
    },
    {
        "map": {"Unf":0,"LwQ":1,"Rec":2,"BLQ":3,"ALQ":4,"GLQ":4},
        "cols": ["BsmtFinType1","BsmtFinType2"]
    },
    {
        "map": {"Sal":1,"Sev":2,"Maj2":3,"Maj1":4,
                "Mod":5,"Min2":6,"Min1":7,"Typ":8},
        "cols": ["Functional"]
    },
    {
        "map": {"Unf":0,"RFn":1,"Fin":2},
        "cols": ["GarageFinish"]
    },
    {
        "map": {"MnWw":1,"GdWo":2,"MnPrv":3,"GdPrv":4},
        "cols": ["Fence"]
    }
]