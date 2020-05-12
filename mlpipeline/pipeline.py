#!/usr/bin/env python
# coding: utf-8

import nltk
from pyspark.conf import SparkConf
from pyspark.ml import Pipeline
from pyspark.ml.clustering import LDA
from pyspark.ml.feature import StopWordsRemover, CountVectorizer, IDF, Tokenizer
from pyspark.sql import SparkSession
import json

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# pyspark creating spark session function
def create_spark_session():
    cf = SparkConf()
    spark = SparkSession.builder.config(conf=cf).getOrCreate()
    return spark


def create_lda_pipeline():
    # hyper-parameters
    num_topics = 10
    max_iterations = 10

    # pipeline
    tokenizer = Tokenizer(inputCol="content", outputCol="tokenized")
    cleaned = StopWordsRemover(inputCol="tokenized", outputCol="cleaned")
    tf = CountVectorizer(inputCol="cleaned", outputCol="raw_features", vocabSize=10, minDF=1.0)
    idf = IDF(inputCol="raw_features", outputCol="features")
    lda_model = LDA(featuresCol="features", k=num_topics, maxIter=max_iterations)
    return Pipeline(stages=[tokenizer, cleaned, tf, idf, lda_model])


spark = create_spark_session()

pipeline = create_lda_pipeline()


# sentiment analyzer function
def sentiment_analysis(data):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(data)
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def get_df_from_json(json_data):
    with open('temp.json', 'w') as f:
        json.dump(json_data, f)
    return spark.read.json('temp.json')


# ml pipeline
def run_ml_pipeline(json_data):
    # handling Nonetype url column
    if 'url' not in json_data or json_data['url'] is None or json_data['url'].strip() == "":
        url = ""
        return [], [], url, 'neutral'
    else:
        url = json_data['url'].strip()

    # handling Nonetype text column
    if 'content' not in json_data or json_data['content'] is None or json_data['content'].strip() == "":
        content = ""
        return [], [], url, 'neutral'
    else:
        content = json_data['content']
    content = content.strip()

    # handling empty text field
    if not content:
        return [], [], url, 'neutral'

    # sentiment analysis
    sentiment_fact = sentiment_analysis(content)

    df = get_df_from_json(json_data)

    # clustering
    model = pipeline.fit(df)
    print("Fit the model successfully")
    topics = model.stages[-1].describeTopics(1)
    vocab = model.stages[2].vocabulary

    # remove duplicates and blank values from vocab
    vocab_fin = [w for w in vocab if w.isalpha()]
    vocab_final = list(set(vocab_fin))
    return topics, vocab_final, url, sentiment_fact


# write into json
def write_to_json(json_data):
    topics, vocab, url, sentiment_fact = run_ml_pipeline(json_data)
    detail = {'url': url, 'vocab': vocab, 'sentiment': sentiment_fact}
    return detail
