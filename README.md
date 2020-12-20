# Twitter Semantic Analysis



## 1. Getting Started

First, please clone this repo

``` bash
git clone https://github.com/duong19/Twitter-Analysis.git
```

Run this script to create environment (you need to install Miniconda or Anaconda first):

``` bash
cd Twitter-Analysis

conda create --name bigdata --file requirements.txt

conda activate bigdata
```
Then run notebook `TwitterModel.ipynb` to get your Pytorch model

## 2. Docker

Run ` docker-compose up --build` to get your docker running

Go to [this url](https://localhost:9870) to see your HDFS file system