import pandas as pd
import string
import re
from nltk.stem import WordNetLemmatizer

# Which columns will you use?
"Series_Title", "Overview", "Genre", "IMDB_Rating"
# Clean your columns
"convert to lower case", "remove puncutations", "expand contractions", "stemming", "lemmatization", "remove extra space"
# Concatenate the columns needed for your embedding
"Series_Title", "Overview","Genre", "IMDB_Rating"
# Create new column with concatenated and clean text
"Series_Title_Overview_Genre_IMDB_Rating"

contraction_mapping = {
    "dont": "do not",
    "wont": "will not",
    "cant": "cannot",
    "shouldve": "should have",
    "its": "it is"
}
lemmatizer = WordNetLemmatizer()


# Read the data from csv and clean data
def readData():
    moviesOriginal = pd.read_csv("imdb_top_1000.csv")
    movies = moviesOriginal[["Series_Title", "Overview", "Genre", "IMDB_Rating"]].copy()

    # Convert to lower case
    movies["Series_Title"] = convert_to_lowercase(movies["Series_Title"])
    movies["Overview"] = convert_to_lowercase(movies["Overview"])
    movies["Genre"] = convert_to_lowercase(movies["Genre"])

    # Remove punctuation to lower case
    movies["Series_Title"] = remove_punctuations(movies["Series_Title"])
    movies["Overview"] = remove_punctuations(movies["Overview"])
    movies["Genre"] = remove_punctuations(movies["Genre"])

    # Expand Contractions
    movies["Series_Title"] = expand_contractions(movies["Series_Title"])
    movies["Overview"] = expand_contractions(movies["Overview"])
    movies["Genre"] = expand_contractions(movies["Genre"])

    # Lemmatization
    movies["Series_Title"] = lemmatization(movies["Series_Title"])
    movies["Overview"] = lemmatization(movies["Overview"])
    movies["Genre"] = lemmatization(movies["Genre"])

    # Remove Extra Spaces
    movies["Series_Title"] = remove_extra_spaces(movies["Series_Title"])
    movies["Overview"] = remove_extra_spaces(movies["Overview"])
    movies["Genre"] = remove_extra_spaces(movies["Genre"])


    moviesOriginal["moviedata"] = "The movie title is " + movies["Series_Title"] + ". An overview of the movie is as follows " + movies["Overview"]+ " and the genre of the movie is " + movies["Genre"] + " and the movie has an imdb rating of " +movies["IMDB_Rating"].astype(str)
    #print(movies.loc[0,"moviedata"])
    return moviesOriginal

# Convert to lowercase
def convert_to_lowercase(df):
    df = df.map(lambda x: x.lower())
    return df


# Remove punctuation
def remove_punctuations(df):
    df = df.map(lambda x: x.translate(str.maketrans("", "", string.punctuation)))
    return df



#-Expanding the contractions
#-don't -> do not
def expand_contractions(df):
    df = df.map(lambda x: " ".join([contraction_mapping.get(word, word) for word in x.split()]))
    return df


# Lemmatizing the words
def lemmatization(df):
    df = df.map(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))
    return df


# Remove extra white spaces, tabs, new lines.
def remove_extra_spaces(df):
    df = df.map(lambda x: " ".join([re.sub(r'\s{2,}', ' ', re.sub(r'\s+', ' ', word)).strip() for word in x.split()]))
    return df