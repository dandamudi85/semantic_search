1) First we need to install the libraries mentioned in requirements.txt
2) To run Elastic Search we need to install Docker Destop for windows.
After installing Docker Destop run the command
( docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.12.1 ) 
3) run the python file create_dataset.py to pull the data from Kaggle. we need kaggle authentication api token for this step.
4) run the python file embed_and_store_data.py to read the data, clean the data and then generate embedding and store the embedding in Elastic Search.
5) run the python file search_app.py using command (streamlit run search_app.py) to run the stream lit app and process the user search.

References:
1) https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows  (Dataset)
2) https://huggingface.co/sentence-transformers/msmarco-MiniLM-L6-cos-v5 (Sentence Transformer Model)
3) https://deysusovan93.medium.com/text-cleaning-the-secret-weapon-for-smarter-nlp-models-6b58dbd594a9 (Used some of the concepts from here to Clean the data)