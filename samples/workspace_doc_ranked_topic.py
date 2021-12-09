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


if len(sys.argv) < 2:
    print("Error! Usage: workspace_doc_ranked_topic.py WORKSPACE_ID <OPTIONAL: TITLE_PHRASE_MATCH>")
    exit(-1)


workspace_id = sys.argv[1]

title_phrase_match = None
if len(sys.argv) >= 3:
    title_phrase_match = sys.argv[2]


# Create the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('############################################')
print('#    Workspace Doc Ranked Topic Example    #')
print('############################################')
print('')
print('')

print(f'Processing ranked topics in workspace {workspace_id}')
print('')

filter_params = None

if title_phrase_match is not None:
    filter_params = {}
    filter_params['title_phrase_match'] = [title_phrase_match]

response = hyperia.workspace_doc_ranked_topic(workspace_id, filter_params=filter_params)

print('## Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

