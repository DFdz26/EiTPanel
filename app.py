import os

from flask import Flask, request, Response, render_template
import numpy as np
import cv2
import jsonpickle
import threading
import base64
import copy
import fakeConnectionSAP as DBConnection
import EiT_integration.BarCoddunication.barcode_reader as barcode_reader
import requests

DEBUG = True
CONNECT_MiR = True
MiR_add = 'http://localhost:5505'

app = Flask(__name__)
dict_change_mir_queue = {
    0: "Stop",
    1: "Start",
    2: "Continue",
}


def request_mir(data, final):
    if DEBUG:
        print(f"Dir arg with value: {data}")

    if CONNECT_MiR:
        headers = {'content-type': "application/json"}
        dic_data = {"place": data, "final": final}

        response = requests.post(MiR_add + '/req', headers=headers, params=dic_data)


def change_mir_queue(data):
    if DEBUG:
        print(f"Change arg with value: {data}.")

        text = f"It corresponds to the action {dict_change_mir_queue[data]}." if data in dict_change_mir_queue \
            else "The specified change is not listed in the options."

        print(text)

    if CONNECT_MiR:
        headers = {'content-type': "application/json"}
        dic_data = {"data": dict_change_mir_queue[data]}

        response = requests.post(MiR_add + '/queue', headers=headers, params=dic_data)


def process_img(received):
    aux = base64.decodebytes(received)
    nparr = np.frombuffer(aux, np.uint8)

    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    code, _ = barcode_reader.adaptive_read(img, imgsize=(4000, 3000), detectionparams=(13, 10, 100),
                                           binarizationparams=(10, 30, 101))

    if DEBUG:
        print("BARCODE:", str(code)[2:-1])

    places = DBConnection.search_item(str(code)[2:-1], DBConnection.DB_NAME)

    if DEBUG:
        print(f"The robot should go to the place: {places[0]}")

    if CONNECT_MiR:
        headers = {'content-type': "application/json"}
        # TODO: Station
        dic_data = {"subs": places[0], "sta": "A"}

        response = requests.post(MiR_add + '/point', headers=headers, params=dic_data)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/picture', methods=['PUT'])
def receive_b64_img():
    r = request
    process = copy.copy(r.data)

    thread = threading.Thread(target=process_img, args=(process, ))
    thread.start()

    response = {'message': 'image received.'}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/state', methods=['POST'])
def change_queue_state():
    r = request
    process = copy.copy(int(r.args["change"]))

    thread = threading.Thread(target=change_mir_queue, args=(process,))
    thread.start()

    response = {'message': 'Order received.'}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/req_robot', methods=['POST'])
def req_robot():
    r = request
    process = copy.copy(r.args["dir"])
    final = 1 if "final" in r.args else 0

    thread = threading.Thread(target=request_mir, args=(process, final))
    thread.start()

    response = {'message': 'Order received.'}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)
