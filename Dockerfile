FROM jupyter/pyspark-notebook
RUN pip install torch torchtext spacy && python -m spacy download en_core_web_md && python -m spacy link en_core_web_md en