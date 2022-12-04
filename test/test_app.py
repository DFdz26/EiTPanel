from __future__ import print_function
import requests
import json
import base64

addr = 'http://localhost:5500'


def send_img():
    test_url = addr + '/picture'
    photo = "test/test8.jpg"

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    # img = open(photo, 'rb').read()

    with open(photo, "rb") as img_file:
        img = base64.b64encode(img_file.read())
    # send http request with image and receive response

    response = requests.put(test_url, data=img, headers=headers)
    # decode response
    return response


def send_req():
    test_url = addr + '/req_robot'

    # prepare headers for http request
    content_type = "application/json"
    headers = {'content-type': content_type}
    dic_data = {"dir": 0}

    response = requests.post(test_url, params=dic_data)
    # decode response
    return response


def send_change_queue(change):
    test_url = addr + '/state'

    # prepare headers for http request
    content_type = "application/json"
    headers = {'content-type': content_type}
    dic_data = {"change": change}

    response = requests.post(test_url, params=dic_data)
    # decode response
    return response


def send_continue():
    return send_change_queue(2)


def send_start():
    return send_change_queue(1)


def send_stop():
    return send_change_queue(0)


options = {
    "SEND_IMG": send_img,
    "CONTINUE": send_continue,
    "STOP": send_stop,
    "START": send_start,
    "REQ": send_req,
}

selected_option = "CONTINUE"

print(options[selected_option]().text)
