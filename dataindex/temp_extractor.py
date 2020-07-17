from utils.kafkahelper import KafkaConnection
from glob import glob
import json

if __name__ == '__main__':
    conn = KafkaConnection()
    for filename in glob('../data/717_20170904123036/717_webhose-2017-01_20170904123520/*.json'):
        with open(filename, encoding="utf8") as f:
            print(filename)
            data = json.load(f)
            conn.send_data(data)
