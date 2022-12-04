import time
from flask import Flask, request, Response
import jsonpickle
import threading

import sys
import os

# get current directory
cwd = os.getcwd()
mir_communication_path = os.path.join(cwd, "EiT_integration")

sys.path.append(mir_communication_path)

from EiT_integration.Integration.integration import Deliverirororirobot
from EiT_integration.MiRCommunication.MiR.MiRCommunication import MIR

CONNECT_MiR = False
DEBUG = True

app = Flask(__name__)

MiR_microservice_ip = 'localhost'
MiR_microservice_port = 5505
auth_file_dir = "EiT_integration/MiRCommunication/auth.json"

taskManager = {
    "list": [],
    "lock": threading.Lock(),
    "condition": threading.Event()
}

event_stop_prog = threading.Event()


event_program_started = threading.Event()
# program_started = {
#     "Value": False,
#     "Lock": threading.Lock()
# }

# initialize MiR communication
mirinterface = MIR(auth_file=auth_file_dir)

# initialize robot
derobot = Deliverirororirobot(mirinterface, 1)


def check_len_list_task():
    with taskManager["lock"]:
        len_ = len(taskManager["list"])

    return len_


def add_point_wrapper(dic):
    station = dic["station"]
    substation = int(dic["substation"])
    wait_ = dic["wait"]

    if DEBUG:
        print(f"Moving the robot to the station '{station}' substation '{substation}'")

    if CONNECT_MiR:
        derobot.move_to_assemblystation(station)
        derobot.move_to_assemblysubpoint(substation)

    if wait_:
        if DEBUG:
            print("Waiting condition")

        taskManager["condition"].wait()

        if DEBUG:
            print("Condition received")

    if 1 == check_len_list_task():

        if DEBUG:
            print("Move_home_wrapper added")

        with taskManager["lock"]:
            helper_dict = {
                "fun": move_home_wrapper,
                "args": {
                    "wait": False,
                    "final": True
                }
            }

            taskManager["list"].append(helper_dict)


def move_warehouse_wrapper(dic):
    wait_ = dic["wait"]
    final = dic["final"]

    if DEBUG:
        text = "Returning to warehouse" if final else "Moving the robot to the warehouse"
        print(text)

    if CONNECT_MiR:
        if final:
            derobot.return_to_warehouse()
        else:
            derobot.move_to_warehouse()

    if wait_:
        if DEBUG:
            print("Waiting condition")

        taskManager["condition"].wait()

        if DEBUG:
            print("Condition received")

    event_program_started.clear()


def move_home_wrapper(dic):
    wait_ = dic["wait"]

    if DEBUG:
        print("Moving robot to home")

    if CONNECT_MiR:
        derobot.move_to_home()

    event_program_started.clear()

    if wait_:
        if DEBUG:
            print("Waiting condition")

        taskManager["condition"].wait()

        if DEBUG:
            print("Condition received")


def check_program_started():
    started = False

    if check_len_list_task():
        started = move_home_wrapper == taskManager["list"][0]["fun"] or \
                  move_warehouse_wrapper == taskManager["list"][0]["fun"]

    if not started:
        started = event_program_started.is_set()

    return started


def taskHandler():

    while not event_stop_prog.is_set():

        if check_program_started():
            taskManager["list"][0]["fun"](taskManager["list"][0]["args"])

            with taskManager["lock"]:
                _ = taskManager["list"].pop(0)

        time.sleep(0.1)


def stop_queue():
    success = False
    message = "There queue hasn't started."

    with taskManager["lock"]:

        if event_program_started.is_set():
            event_program_started.clear()

            taskManager["list"] = []

            helper_dict = {
                "fun": move_home_wrapper,
                "args": {
                    "wait": False
                }
            }

            taskManager["list"].append(helper_dict)

            message = ""
            success = True

    return success, message


def start_queue():
    success = False
    message = "There is no queue for starting."

    if check_len_list_task():
        event_program_started.set()

        success = True
        message = ""

    return success, message


def continue_queue():
    success = False
    message = "The queue hasn't been started."

    if event_program_started.is_set():
        taskManager["condition"].set()

        success = True
        message = ""

    return success, message


dict_state_queue = {
    "Stop": stop_queue,
    "Start": start_queue,
    "Continue": continue_queue
}


@app.route('/point', methods=['POST'])
def add_point():
    station = request.args.get('sta')
    substation = request.args.get('subs')
    message_resp = 'Point received.'

    with taskManager["lock"]:

        helper_dict = {
            "fun": add_point_wrapper,
            "args": {
                "station": station,
                "substation": substation,
                "wait": True
            }
        }

        taskManager["list"].append(helper_dict)

    if DEBUG:
        print(message_resp)

    response = {'message': message_resp}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/req', methods=['POST'])
def req_MiR():
    req_station = int(request.args.get('place'))
    final = int(request.args.get('final'))

    status = 419
    message_resp = f"The station '{req_station}' is not inside of the options, only the station 0 (warehouse) " \
                   f"has been implemented."

    if req_station == 0:
        status = 201
        message_resp = "Requested MiR."

        with taskManager["lock"]:
            helper_dict = {
                "fun": move_warehouse_wrapper,
                "args": {
                    "wait": False,
                    "final": final
                }
            }

            taskManager["list"].append(helper_dict)

    if DEBUG:
        print(message_resp)

    response = {'message': message_resp}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=status, mimetype="application/json")


@app.route('/queue', methods=['POST'])
def change_queue_state():
    state = request.args.get('data')
    status = 419
    message_resp = f"The option '{state}' is not inside of the options"

    if state in dict_state_queue:
        status = 201
        message_resp = f"Option '{state}' received correctly"

        success, mess = dict_state_queue[state]()

        if not success:
            message_resp += f" but it couldn't be done. Reason: {mess}"
            status = 420

    if DEBUG:
        print(message_resp)

    response = {'message': message_resp}

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=status, mimetype="application/json")


if __name__ == "__main__":
    thread = None

    if CONNECT_MiR:
        derobot.move_to_home()
    else:
        derobot.robotstate = ['home',0]

    try:
        thread = threading.Thread(target=taskHandler)
        thread.start()
        app.run(host=MiR_microservice_ip, port=MiR_microservice_port, debug=False)
    except KeyboardInterrupt:
        event_stop_prog.set()
        taskManager["condition"].set()

        if thread is not None:
            thread.join()
    finally:
        event_stop_prog.set()
        taskManager["condition"].set()

        if thread is not None:
            thread.join()
