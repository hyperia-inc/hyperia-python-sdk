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
    print("Error! Usage: workspace_delete.py WORKSPACE_GUID")
    exit(-1)


workspace_guid = sys.argv[1]


# Delete the Hyperia Object
hyperia = Hyperia()


print('')
print('')
print('############################################')
print('#        Workspace Delete Example          #')
print('############################################')
print('')
print('')

print(f'Processing delete workspace {workspace_guid}')
print('')

response = hyperia.workspace_delete(workspace_guid)

print('## Response Object ##')
print(json.dumps(response, indent=4))

print('')
print('')
print('')

workspace_id = response['workspace_id']

time.sleep(3)

response = hyperia.workspace_delete(workspace_id)
