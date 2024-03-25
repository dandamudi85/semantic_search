# Which columns will you use?
"Series_Title","Overview","Genre","IMDB_Rating"
# Clean your columns
"convert to lower case","remove puncutations","expand contractions","stemming","lemmatization", "remove extra space"
# Concatenate the columns needed for your embedding
"Series_Title","Overview,Genre","IMDB_Rating"
# Create new column with concatenated and clean text
"Series_Title","Overview_Genre","IMDB_Rating"

import pandas as pd

movies = pd.read_csv("imdb_top_1000.csv")
title = movies[["Series_Title"]]
overview = movies[["Overview"]]
genre = movies[["Genre"]]
rating = movies[["IMDB_Rating"]]
print(title.loc[0])
#print(movies.columns)