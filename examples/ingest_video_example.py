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


if len(sys.argv) < 3:
    print("Error! Usage: ingest_file_example.py FILE WORKSPACE_ID")
    exit(-1)


media_file = sys.argv[1]
workspace_id = sys.argv[2]


recording_title = "Demo Ingestion"
recording_date = "2019-12-11"
recording_time = "10:40:00-0700"


# Create the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('############################################')
print('#       Ingest Media File Example          #')
print('############################################')
print('')
print('')

print('Processing media file: ', media_file)
print('')

response = hyperia.queue_media_file_ingestion(media_file, workspace_id, recording_title, recording_date, recording_time)

print('## Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

