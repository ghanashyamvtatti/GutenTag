from subprocess import run
from flask import Flask
from flask import request
from utils.kafkahelper import KafkaConnection
from threading import Thread

app = Flask(__name__)

STATUS = 'READY'

status_conn = KafkaConnection(topic="status")


# thread process to update the status
def status_listener():
    global STATUS
    for data in status_conn.get_data():
        if data is not None:
            STATUS = data['status']


status_thread = Thread(target=status_listener)


# Begin data extraction
@app.route("/extract")
def start_data_extraction():
    global STATUS
    q = request.args['q']
    proc = run(['echo', q], capture_output=True)
    return {"message": proc.stdout.strip().decode('utf-8'), "status": STATUS}, 200


# Return data from elasticsearch
@app.route("/results")
def show_results():
    if 'limit' in request.args:
        limit = request.args['limit']
    else:
        limit = 100

    if 'offset' in request.args:
        offset = request.args['offset']
    else:
        offset = 0
    # TODO: Get data from elasticsearch and show to the user
    data = {"results": [{"url": "https://www.dudurudh.com/2020/04/25/4-minute-miles-chapter-3/",
                         "tags": ["Seemapuram", "area", "Rambo"], "sentiment": "positive"},
                        {"url": "https://www.dudurudh.com/2020/04/25/4-minute-miles-chapter-3/",
                         "tags": ["Seemapuram", "area", "Rambo"], "sentiment": "positive"},
                        {"url": "https://www.dudurudh.com/2020/04/25/4-minute-miles-chapter-3/",
                         "tags": ["Seemapuram", "area", "Rambo"], "sentiment": "positive"},
                        {"url": "https://www.dudurudh.com/2020/04/25/4-minute-miles-chapter-3/",
                         "tags": ["Seemapuram", "area", "Rambo"], "sentiment": "positive"}]}
    return data, 200


@app.route("/status")
def get_status():
    global STATUS
    return STATUS, 200


if __name__ == '__main__':
    status_thread.start()
    app.run()
