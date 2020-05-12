import sys

from elasticsearch import Elasticsearch

from utils.kafkahelper import KafkaConnection

PORT = 9200
INDEXNAME = "data"
host = "localhost:%s" % PORT
es = Elasticsearch([host])


def get_raw_data(query):
    items = []
    offset = 0
    limit = 100
    # By default, the limit is 10
    while True:
        response = es.search(index=INDEXNAME, q=query, size=limit, from_=offset)
        data = response['hits']['hits']
        if len(data) == 0:
            break
        items += data
        offset += limit
    return items


def push_data(data):
    conn = KafkaConnection()
    for item in data:
        conn.send_data(item["_source"]["doc"])


def main(args):
    status_conn = KafkaConnection(topic='status')
    status_conn.send_data({'status': 'DATA EXTRACTION'})
    if len(args) < 2:
        sys.exit("Incorrect number of arguments")

    data = get_raw_data(args[1])
    status_conn.send_data({'status': 'ML PIPELINE', 'count': len(data)})

    push_data(data)


if __name__ == "__main__":
    main(sys.argv)
