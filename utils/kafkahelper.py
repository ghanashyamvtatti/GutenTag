from pykafka import KafkaClient
import json


class KafkaConnection(object):
    def __init__(self, hosts='127.0.0.1:9092', topic='data'):
        """
        Kafka connection object that serves as a wrapper to quickly push and fetch data from kafka topics
        :param hosts: Comma separated hosts
        :param topic: Topic name
        """
        self.client = KafkaClient(hosts=hosts)
        self.topic = self.client.topics[topic]
        self.consumer = self.topic.get_simple_consumer()

    def send_data(self, data):
        """
        Send data to a topic
        :param data:
        :return:
        """
        with self.topic.get_sync_producer() as producer:
            producer.produce(json.dumps(data).encode())

    def get_data(self):
        """
        A generater to get data from a topic
        example usage: for data from conn.get_data()
        :return:
        """
        for message in self.consumer:
            if message is not None:
                yield json.loads(message.value.decode('utf-8'))
