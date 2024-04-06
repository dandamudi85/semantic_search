"""
    Create an Streamlit app that does the following:

    - Reads an input from the user
    - Embeds the input
    - Search the vector DB for the entries closest to the user input
    - Outputs/displays the closest entries found
"""
import streamlit as st
import pandas as pd
import string
import re
from nltk.stem import WordNetLemmatizer
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
contraction_mapping = {
    "dont": "do not",
    "wont": "will not",
    "cant": "cannot",
    "shouldve": "should have",
    "its": "it is"
}
lemmatizer = WordNetLemmatizer()

def elasticSearch():
    esClient = Elasticsearch("http://localhost:9200")
    print(esClient.info().body)
    return esClient

def embedQuery(query):
    model = SentenceTransformer("msmarco-MiniLM-L6-cos-v5")
    embedding = model.encode(preProcessQuery(query))
    return embedding

def preProcessQuery(query):
    query = query.lower()
    query = query.translate(str.maketrans("", "", string.punctuation))
    query = " ".join([contraction_mapping.get(word, word) for word in query.split()])
    query = " ".join([lemmatizer.lemmatize(word) for word in query.split()])
    query = " ".join([re.sub(r'\s{2,}', ' ', re.sub(r'\s+', ' ', word)).strip() for word in query.split()])
    return query


def searchES(esClient,value):
    try:
        response = esClient.search(index="moviedata_index",knn={"field": "moviedata_embeddings", "query_vector": value, "k": 30, "num_candidates": 100},size=30)
        print(response)
        response = response["hits"]["hits"]
        print("Response Size:",len(response))
        dataList = []
        for hit in response:
            dataList.append({"Movie":hit["_source"]["Series_Title"], "Overview":hit["_source"]["Overview"], "Genre":hit["_source"]["Genre"], "IMBD Rating":str(hit["_source"]["IMDB_Rating"])})
        result = pd.DataFrame(dataList)
        print("Result",result)
        return result
    except Exception as e:
        print("Error while querying ES")
        print(e)

def streamlitDisplay():
    st.write("""
    # Movie Search
    """)
    st.text_input("Search", key="search", label_visibility="hidden",placeholder="Search using Movie Title, Overview, Genre")
    if(st.session_state.search != ""):
        value = st.session_state.search
        print("Value:", value)
        esClient = elasticSearch()
        result = searchES(esClient,embedQuery(value))
        st.title("Search Results")
        st.table(result)
        # st.title("Lexical Search")
        # lexicalResult = searchESLexical(esClient,value)
        # st.table(lexicalResult)


streamlitDisplay()