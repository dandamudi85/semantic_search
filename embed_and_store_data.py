import elasticsearch
from clean_data import readData
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

"""
- Prepare the text to embed for each reccord of your dataset.
    - Create the reccord.
        - Clean the text.
        - Concatenate fields.
- Choose a Sentence Embedding Model.
- Embed the text generated in the previous step for each reccord.
- Store the embeddings in a vector database (i.e. elasticsearch).
"""

def elasticSearch():
    esClient = Elasticsearch("http://localhost:9200")
    print(esClient.info().body)
    getIndex(esClient)
    return esClient

def createIndex(esClient):
    mappings = {
        "properties": {
            "moviedata": {"type": "text"},
            "Series_Title": {"type": "text"},
            "Overview" :  {"type": "text"},
            "Genre" : {"type": "text"},
            "IMDB_Rating" : {"type": "text"},
            "moviedata_embeddings": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
            },
        }
    }
    print(esClient.indices.create(index="movie_index",mappings=mappings))

def getIndex(esClient):
    try:
        response = esClient.indices.get(index="movie_index")
        print("Index response:",response)
    except(elasticsearch.NotFoundError):
        createIndex(esClient)


# Print the embeddings
def printEmbeddings(sentences,embeddings):
    for sentence, embedding in zip(sentences, embeddings):
        print("Sentence:", sentence)
        print("Embedding:", embedding)
        print("")

def storeEmbeddings(sentences,embeddings,esClient):
    for i, row in sentences.iterrows():
        #print(row)
        doc = {
            "moviedata" : row["moviedata"],
            "Series_Title": row["Series_Title"],
            "Overview": row["Overview"],
            "Genre": row["Genre"],
            "IMDB_Rating": row["IMDB_Rating"],
            "moviedata_embeddings" : embeddings[i]
        }
        #print(doc)
        esClient.index(index="moviedata_index",id=i,document=doc)


# Our sentences to encode
def encodeSentences():
    sentences = readData()
    #print(sentences)
    # Sentences are encoded by calling model.encode()
    model = SentenceTransformer("all-mpnet-base-v2")
    embeddings = model.encode(sentences["moviedata"])
    esClient = elasticSearch()
    #printEmbeddings(sentences,embeddings)
    #Store the embeddings in Elastic CLient
    storeEmbeddings(sentences,embeddings,esClient)
    esClient.close()

encodeSentences()
