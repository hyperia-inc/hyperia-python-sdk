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
import time


if len(sys.argv) < 2:
    print("Error! Usage: e2e_ingest_and_query.py WORKSPACE_NAME FILE_URL <OPTIONAL: FILE_TITLE>")
    exit(-1)


workspace_name = sys.argv[1]
media_file = sys.argv[2]
media_title = ''
if len(sys.argv) > 3:
    media_title = sys.argv[3]



# Create the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('######################################################')
print('#        Workspace Ingest and query Example          #')
print('######################################################')
print('')
print('')

print(f'Processing create workspace {workspace_name}')
print('')

response = hyperia.workspace_create(workspace_name)

print('## Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

workspace_id = response['workspace_id']

time.sleep(10)

print('Ingesting file..')

recording_title = "Demo Ingestion"
recording_date = "2019-12-11"
recording_time = "10:40:00-0700"

ingest_response = hyperia.queue_media_file_ingestion(media_file, workspace_id, recording_title, recording_date, recording_time)

print('## Response Object ##')
print(json.dumps(ingest_response, indent=4))

print('')
print('')
print('')

doc_id = ingest_response['guid']

print(f'Doc ID = {doc_id}')

while True:
    print('Polling for ingestion completion..')

    exists_response = hyperia.workspace_doc_exists(workspace_id, doc_id)

    print('## Doc Exists Response Object ##')
    print(json.dumps(exists_response, indent=4))

    print('')
    print('')
    print('')

    if 'exists' in exists_response and exists_response['exists'] == True:
        print('Ingest complete')
        break

    time.sleep(60)

print('Getting doc info..')

response = hyperia.workspace_doc_metadata_info(workspace_id, doc_id)

print('## Metadata Info Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

print('Getting doc transcript..')

response = hyperia.workspace_doc_metadata_transcript(workspace_id, doc_id)

print('## Metadata Transcript Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

print('Getting doc summary..')

response = hyperia.workspace_doc_metadata_summary(workspace_id, doc_id)

print('## Metadata Summary Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

print('Getting topics aggregation..')

topics_response = hyperia.workspace_doc_ranked_topic(workspace_id)

print('## Metadata Topics Response Object ##')
print(json.dumps(topics_response, indent=4))


response = hyperia.workspace_delete(workspace_id)



