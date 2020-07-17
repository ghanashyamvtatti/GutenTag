from subprocess import Popen
from flask import Flask
from flask import request
from utils.kafkahelper import KafkaConnection
from threading import Thread
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__, static_folder='../UI/app/build', static_url_path='/')

CORS(app)

STATUS = {'status': 'READY'}

status_conn = KafkaConnection(topic="status")

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


# thread process to update the status
def status_listener():
    global STATUS
    for data in status_conn.get_data():
        if data is not None:
            STATUS = data


status_thread = Thread(target=status_listener)


# Begin data extraction
@app.route("/extract")
def start_data_extraction():
    global STATUS
    q = request.args['q']
    Popen(['python', '-m', 'dataindex.local_data_extractor', q])
    STATUS['status'] = 'BEGINNING DATA EXTRACTION'
    return {"message": "started data extraction", "status": STATUS}, 200


# Return data from elasticsearch
@app.route("/results")
def show_results():
    q = request.args['q']
    if 'limit' in request.args:
        limit = request.args['limit']
    else:
        limit = 10

    if 'offset' in request.args:
        offset = request.args['offset']
    else:
        offset = 0
    # Get data from elasticsearch and show to the user
    response = es.search(index='articles', q=q, from_=offset, size=limit)
    data = response['hits']['hits']
    data = [x['_source'] for x in data]
    return {'results': data}, 200


@app.route("/status")
def get_status():
    global STATUS
    return STATUS, 200


if __name__ == '__main__':
    status_thread.start()
    app.run()
