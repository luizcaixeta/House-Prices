from kaggle.api.kaggle_api_extended import KaggleApi
import os
import zipfile

def data_collection():

    api = KaggleApi()
    api.authenticate()

    os.makedirs("../data", exist_ok=True)

    api.competition_download_files(
        "house-prices-advanced-regression-techniques",
        path="../data",
    )

    for f in os.listdir("../data"):
        if f.endswith(".zip"):
            zip_path = os.path.join("../data", f)

            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall("../data")

            os.remove(zip_path)
            print(f"Descompactado: {f}")