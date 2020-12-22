FROM jupyter/pyspark-notebook
RUN pip install torch torchtext spacy tweepy kafka-python && python -m spacy download en_core_web_md && python -m spacy link en_core_web_md en


