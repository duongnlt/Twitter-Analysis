FROM jupyter/pyspark-notebook
RUN pip install torch torchtext spacy tweepy kafka-python && python -m spacy download en_core_web_md && python -m spacy link en_core_web_md en


FROM node:14
WORKDIR /usr/app/streaming

COPY ./streaming/package.json ./
COPY ./streaming/package-lock.json ./

RUN npm install --quiet

COPY ./streaming .

# ENV TZ=Asia/Ho_Chi_Minh
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone