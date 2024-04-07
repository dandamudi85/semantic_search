import kaggle
import zipfile

kaggle.api.authenticate()
dataset = "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"
kaggle.api.dataset_download_files(dataset)

#Extracts the contents from ZIP file
with zipfile.ZipFile(
    "imdb-dataset-of-top-1000-movies-and-tv-shows.zip", "r"
) as zip_ref:
    zip_ref.extractall(".")