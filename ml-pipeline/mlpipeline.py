#!/usr/bin/env python
# coding: utf-8

from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import StopWordsRemover, CountVectorizer, IDF, Tokenizer
from pyspark.ml.clustering import LDA
from pyspark.ml import Pipeline
import json
import nltk
nltk.download('vader_lexicon')
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#sentiment analyzer function
def sentiment_analysis(data):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(data)
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

#pyspark creating spark session function
def create_spark_session():
    cf = SparkConf()
    spark = SparkSession.builder.config(conf = cf).getOrCreate()
    return spark

#ml pipeline
def ml_pipeline(jsondata):
    spark = create_spark_session()
    df = spark.read.json(jsondata)
    data = df.select('url', 'text').where(df['text'] != '')
    url = data.select('url').head()['url']
    text_sentiment = data.select('text').head()['text']
    text_sentiment = text_sentiment.strip()

    #handling empty text field
    if (not text_sentiment):
        return [], [], url, 'neutral'

    #sentiment analysis
    sentiment_fact = sentiment_analysis(text_sentiment)

    #hyper-parameters
    num_topics = 10
    max_iterations = 100

    #pipeline
    tokenizer = Tokenizer(inputCol="text", outputCol="tokenized")
    cleaned = StopWordsRemover(inputCol="tokenized", outputCol="cleaned")
    tf = CountVectorizer(inputCol="cleaned", outputCol="raw_features", vocabSize=10, minDF=1.0)
    idf = IDF(inputCol="raw_features", outputCol="features")
    lda_model = LDA(featuresCol="features", k=num_topics, maxIter=max_iterations)
    pipeline = Pipeline(stages=[tokenizer, cleaned, tf, idf, lda_model])

    #clustering
    model = pipeline.fit(data)
    topics = model.stages[-1].describeTopics(1)
    vocab = model.stages[2].vocabulary
    return topics, vocab, url, sentiment_fact

#write into json
def write_to_json(jsondata):
    topics, vocab, url, sentiment_fact = ml_pipeline(jsondata)
    detail = {'url': url, 'vocab': vocab, 'sentiment': sentiment_fact}
    return detail