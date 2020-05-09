from pykafka import KafkaClient
import json


class KafkaConnection(object):
    def __init__(self, hosts='127.0.0.1:9092', topic='data'):
        self.client = KafkaClient(hosts=hosts)
        self.topic = self.client.topics[topic]
        self.consumer = self.topic.get_simple_consumer()

    def send_data(self, data):
        with self.topic.get_sync_producer() as producer:
            producer.produce(json.dumps(data).encode())

    def get_data(self):
        for message in self.consumer:
            if message is not None:
                yield json.loads(message.value.decode('utf-8'))
