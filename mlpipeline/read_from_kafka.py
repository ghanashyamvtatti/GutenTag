from utils.kafkahelper import KafkaConnection

conn = KafkaConnection()


def do_something(data):
    print(data)


if __name__ == '__main__':
    for data in conn.get_data():
        do_something(data)
