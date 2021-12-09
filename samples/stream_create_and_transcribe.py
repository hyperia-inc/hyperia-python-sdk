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


def sender_thread(ws, file):
    print("Starting sender loop.")
    bytes = file.read(640)
    while bytes:
        ws.send_binary(bytes)

        bytes = file.read(640)

        time.sleep(0.02)
    print("Finished sending")


def receiver_thread(ws):
    print("Starting receiver loop.")
    while True:
        message = ws.recv()

        print(message)
    print("Receiver exiting")


def open_websockets(socket_id, audio_socket, event_socket, file_path):
    print(f"Connencting to socket {socket_id}")

    ws_send = websocket.WebSocket()
    socket_url = audio_socket
    print(socket_url)
    ws_send.connect(socket_url)

    ws_recv = websocket.WebSocket()
    socket_url = event_socket
    print(socket_url)
    ws_recv.connect(socket_url)

    print("Connected..")

    file = open(file_path, "rb")

    send_thread = threading.Thread(target=sender_thread, args=(ws_send, file))

    recv_thread = threading.Thread(target=receiver_thread, args=(ws_recv,))

    print("Starting receiver.")
    recv_thread.start()

    print("Starting sender.")
    send_thread.start()

    send_thread.join()


if len(sys.argv) < 2:
    print("Error! Usage: stream_create_and_transcribe.py <FILENAME")
    exit(-1)


file_path = sys.argv[1]


# Create the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('############################################')
print('#      Create Streaming ASR Example        #')
print('############################################')
print('')
print('')


response = hyperia.stream_create()

print('## Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

stream_id = response['result']['stream_id']

print(f"Created stream {stream_id}")

audio_socket = response['result']['audio_socket']
event_socket = response['result']['event_socket']

open_websockets(stream_id, audio_socket, event_socket, file_path)

