from kaggle.api.kaggle_api_extended import KaggleApi
import os
import zipfile

def data_collection():

    api = KaggleApi()
    api.authenticate()

    path = "../data/raw"

    os.makedirs(path , exist_ok=True)

    api.competition_download_files(
        "house-prices-advanced-regression-techniques",
        path=path,
    )

    for f in os.listdir(path):
        if f.endswith(".zip"):
            zip_path = os.path.join(path, f)

            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(path)

            os.remove(zip_path)
            print(f"Descompactado: {f}")