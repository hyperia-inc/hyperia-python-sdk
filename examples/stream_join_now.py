#!/usr/bin/env python

#	Copyright 2021 Hyperia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
from hyperia import Hyperia
import json
import sys
import websocket
import time
import threading
import json
import requests
import uuid


def receiver_thread(ws):
    print("Starting receiver loop.")
    while True:
        message = ws.recv()
        json_message = json.loads(message)

        if json_message['document_type'] == 'h:fm:SpeechToTextLive':
            continue

        if json_message['document_type'] == 'h:fm:SpeechToText':
            continue

        print(message)
        print("")
    print("Receiver exiting")


def open_websockets(event_socket):
    print(f"Connencting to socket")

    ws_recv = websocket.WebSocket()
    socket_url = event_socket
    print(socket_url)
    ws_recv.connect(socket_url)

    print("Connected..")

    recv_thread = threading.Thread(target=receiver_thread, args=(ws_recv,))

    print("Starting receiver.")
    recv_thread.start()

    recv_thread.join()


if len(sys.argv) < 2:
    print("Error! Usage: stream_join_now.py <MEETING_URL> <Optional:MEETING_PASSWORD>")
    exit(-1)


meeting_link = sys.argv[1]
meeting_password = ''
if len(sys.argv) > 2:
    meeting_password = sys.argv[2]


# Create the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('############################################')
print('#      Join and Stream Meeting Example     #')
print('############################################')
print('')
print('')


response = hyperia.meeting_join(meeting_link, meeting_password, index_data=False, live_stream=True)

print(response)

meeting_guid = response['result']['meeting_data']['meeting_guid']


print(f"Got meeting guid: {meeting_guid}")

event_socket = None

while True:
    response = hyperia.meeting_info(meeting_guid)
    print(response)
    if 'stream_data' in response['result']:
        if 'event_socket' in response['result']['stream_data']:
            event_socket = response['result']['stream_data']['event_socket']
            break
    time.sleep(15)
    
print("Got event socket.")

time.sleep(3)

print("Opening websockets..")

open_websockets(event_socket)

