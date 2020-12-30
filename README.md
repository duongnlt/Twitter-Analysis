# Twitter Semantic Analysis



## 1. Getting Started

First, please clone this repo

``` bash
git clone https://github.com/duong19/Twitter-Analysis.git
```

Run this script

``` bash
cd Twitter-Analysis

cd streaming

npm install

```


## 2. Docker

Execute this script to get your docker running
 ```
 docker-compose up --build
 ``` 


Open Pyspark Notebook, run file **spark_streaming.ipynb** then **hadoop_stream.ipynb**


## 3. Visualize
Run Flask server (make sure kafka has data first):
```
cd flask

export FLASK_APP=app.py

flask run
```

Go to [this url](https://localhost:5000) to see your graphs