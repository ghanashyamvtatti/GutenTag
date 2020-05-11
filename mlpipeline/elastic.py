#!/usr/bin/env python
# coding: utf-8


from mlpipeline import pipeline
from elasticsearch import Elasticsearch
from utils.kafkahelper import KafkaConnection


def main():
    conn = KafkaConnection()
    # download es and keep it running on the local sys while executing this
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # data = "717_20170904123036/717_webhose-2017-01_20170904123520/blogs_0000001.json"
    id = 0
    # set up of index for es
    index = 'articles'
    doc_type = 'article'

    for data in conn.get_data():
        detail = pipeline.write_to_json(data)
        # insert json into elasticsearch
        id += 1
        store = es.index(index=index, doc_type=doc_type, id=id, body=detail)
        print(store)
        # just to retrieve data from es
        retrieve = es.get(index=index, doc_type=doc_type, id=id)
        print(retrieve['_source'])
        # deleting the document(this statement can be deleted later)
        erase = es.delete(index=index, doc_type=doc_type, id=id)
        print(erase['result'])


if __name__ == '__main__':
    main()
