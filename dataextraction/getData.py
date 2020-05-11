import urllib3
import sys
import json
from utils.kafkahelper import KafkaConnection

PORT = 9200
INDEXNAME = "data"
host = "localhost:%s"%PORT


def getRawData(query,count=5):
    http = urllib3.PoolManager()
    url = "http://%s/data/_search?q=%s&size=%s"%(host,query,str(count))
    response = http.request(method="GET",url=url).data
    data = json.loads(response.decode('utf-8'))
    items = data["hits"]["hits"]
    return items

def pushData(data):
    conn = KafkaConnection()
    for item in data:
        conn.send_data(item["_source"]["doc"])

def main(args):
    if len(args)< 2:
        sys.exit("Incorrect number of arguments")
    
    data = None
    if len(args) == 3:
        data = getRawData(args[1],args[2])
    else:
        data = getRawData(args[1])

    pushData(data)

if __name__ == "__main__":
    main(sys.argv)
