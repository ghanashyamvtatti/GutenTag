import elasticsearch
from elasticsearch.helpers import bulk, scan
import os
import json
import sys

dataDir = "G:\Rochak\Downloads\Data"
PORT = 9200
INDEXNAME = "data"

DIRS = [os.path.join(dataDir, o) for o in os.listdir(dataDir) if os.path.isdir(os.path.join(dataDir,o))]
host = "Localhost:%s"%PORT
global es
es = elasticsearch.Elasticsearch([host])
print(es.info())

def processDir(dir,indexName):
    files = os.listdir(dir)
    for file in files:
        file = os.path.join(dir,file)
        with open(file) as f:
            try:
                data = json.load(f)
                body = {}
                body['url'] = data["url"]
                body['content'] = data["text"]
                item = {}
                item["_index"] = indexName
                item["doc"] = body
                yield item
            except:
                print("Error in: ",file)
                continue

def createIndex(indexName = "data"):
    item={"mappings": {
                        "properties": {
                            "url": {"type": "text", "index": False},
                            "content": {"type": "text"},
                                        }
                                }
    }
    try:
        response = es.indices.create(index=indexName,body=item)
        print(response)
        if response["acknowledged"]==True:
            print("Index %s created successfully"%indexName)
            return False
        else:
            print("Error in creating Index %s"%indexName)
            return True
    except Exception as e:
        return True
        print("Error: ",e)

def main():
    err = createIndex(INDEXNAME)
    if err:
        sys.exit("Check index creation errors")
    for dir in DIRS:
        print("Indexing: ",dir)
        bulk(es,processDir(dir,INDEXNAME))
    print("Initialization completed")

if __name__ == "__main__":
    main()