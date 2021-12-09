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

import requests
import uuid

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json


class Hyperia:
    # Setup the endpoints
    ENDPOINTS = {}
    ENDPOINTS['ingest'] = {}
    ENDPOINTS['ingest']['file'] = '/v1/workspace/id/{workspace_id}/ingest/file'
    ENDPOINTS['ingest']['url'] = '/v1/workspace/id/{workspace_id}/ingest/url'
    ENDPOINTS['bot'] = {}
    ENDPOINTS['bot']['meeting_join'] = '/v1/meeting/join'
    ENDPOINTS['bot']['meeting_list'] = '/v1/meeting/list'
    ENDPOINTS['bot']['meeting_info'] = '/v1/meeting/id/{meeting_id}/metadata/info'
    ENDPOINTS['bot']['meeting_exists'] = '/v1/meeting/id/{meeting_id}/exists'
    ENDPOINTS['stream'] = {}
    ENDPOINTS['stream']['stream_create'] = '/v1/stream/create'
    ENDPOINTS['stream']['stream_list'] = '/v1/stream/list'
    ENDPOINTS['stream']['stream_exists'] = '/v1/stream/id/{stream_id}/exists'
    ENDPOINTS['workspace'] = {}
    ENDPOINTS['workspace']['list'] = '/v1/workspace/list'
    ENDPOINTS['workspace']['public_list'] = '/v1/workspace/public/list'
    ENDPOINTS['workspace']['doc_search_transcript'] = '/v1/workspace/id/{workspace_id}/doc/search/transcript'
    ENDPOINTS['workspace']['doc_list'] = '/v1/workspace/id/{workspace_id}/doc/list'
    ENDPOINTS['workspace']['doc_delete'] = '/v1/workspace/id/{workspace_id}/doc/{doc_id}'
    ENDPOINTS['workspace']['doc_ranked_topic'] = '/v1/workspace/id/{workspace_id}/doc/ranked/topic'
    ENDPOINTS['workspace']['doc_ranked_tag'] = '/v1/workspace/id/{workspace_id}/doc/ranked/tag'
    ENDPOINTS['workspace']['doc_ranked_speaker'] = '/v1/workspace/id/{workspace_id}/doc/ranked/speaker'
    ENDPOINTS['workspace']['doc_exists'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/exists'
    ENDPOINTS['workspace']['doc_metadata_info'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/info'
    ENDPOINTS['workspace']['doc_metadata_transcript'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/transcript'
    ENDPOINTS['workspace']['doc_metadata_summary'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/summary'
    ENDPOINTS['workspace']['doc_metadata_monologues'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/monologues'
    ENDPOINTS['workspace']['doc_metadata_topics'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/topics'
    ENDPOINTS['workspace']['doc_metadata_tags'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/tags'
    ENDPOINTS['workspace']['doc_metadata_concepts'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/concepts'
    ENDPOINTS['workspace']['doc_metadata_screens'] = '/v1/workspace/id/{workspace_id}/doc/id/{doc_id}/metadata/screens'
    ENDPOINTS['management'] = {}
    ENDPOINTS['management']['workspace_create'] = '/v1/management/workspace/create'
    ENDPOINTS['management']['workspace_delete'] = '/v1/management/workspace/delete/{workspace_id}'

    # The base URL for all endpoints
    BASE_URL = 'https://api.hyperia.net'


    s = requests.Session()

    def __init__(self):
        """	
        Initializes the SDK so it can send requests to Hyperia for analysis.
        It loads the API key from api_key.txt and configures the endpoints.
        """

        import sys
        try:
            # Open the key file and read the key
            f = open("api_key.txt", "r")
            key = f.read().strip()

            if key == '':
                # The key file should't be blank
                print(
                    'The api_key.txt file appears to be blank, please run: python hyperia.py YOUR_KEY_HERE')
                print(
                    'If you do not have an API Key from Hyperia, please register for one at: http://www.hyperia.com/api/register.html')
                sys.exit(0)
            elif len(key) != 73:
                # Keys should be exactly 73 characters long
                print(
                    'It appears that the key in api_key.txt is invalid. Please make sure the file only includes the API key, and it is the correct one.')
                sys.exit(0)
            else:
                # setup the key
                self.apikey = key

            # Close file
            f.close()
        except IOError:
            # The file doesn't exist, so show the message and create the file.
            print(
                'API Key not found! Please run: python hyperia.py YOUR_KEY_HERE')
            print(
                'If you do not have an API Key from Hyperia, please register for one at: http://www.hyperia.com/api/register.html')

            # create a blank key file
            open('api_key.txt', 'a').close()
            sys.exit(0)
        except Exception as e:
            print(e)

    def workspace_create(self, workspace_name):
        """

        INPUT:
        workspace_name -> name of the new workspace

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'workspace_create'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['management']:
            return {'status': 'ERROR', 'statusInfo': 'management API ' + flavor + ' not available'}

        put_data = {'workspace_name': workspace_name}

        real_url = Hyperia.ENDPOINTS['management'][flavor]

        return self.__put(real_url, put_data)

    def workspace_delete(self, workspace_id):
        """

        INPUT:
        workspace_id -> id of the new workspace

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'workspace_delete'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['management']:
            return {'status': 'ERROR', 'statusInfo': 'management API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['management'][flavor].replace("{workspace_id}", workspace_id)

        return self.__delete(real_url)

    def ingest_url(self, workspace_id, media_url, media_title=''):
        """

        INPUT:
        media_url -> http or https link to a video or audio file
        media_title -> (optional) title for the ingested file

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'url'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['ingest']:
            return {'status': 'ERROR', 'statusInfo': 'ingest API ' + flavor + ' not available'}

        put_data = {'url': media_url}

        if len(media_title) > 0:
            put_data['title'] = media_title

        real_url = Hyperia.ENDPOINTS['ingest'][flavor].replace("{workspace_id}", workspace_id)

        return self.__put(real_url, put_data)

    def stream_create(self):
        """

        INPUT:
        None

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'stream_create'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['stream']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        put_data = {}

        real_url = Hyperia.ENDPOINTS['stream'][flavor]

        return self.__put(real_url, put_data)

    def stream_list(self):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'stream_list'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]

        return self.__get(real_url)

    def stream_exists(self, stream_id):
        """

        INPUT:
        stream_id -> stream ID

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'stream_exists'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]
        real_url = real_url.replace("{stream_id}", meeting_id)

        return self.__get(real_url)

    def meeting_join(self, meeting_link, meeting_password='', index_data=True, live_stream=False):
        """

        INPUT:
        meeting_link -> link of a Zoom, Google Meet, or Teams call
        meeting_password -> (optional) password for the call

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'meeting_join'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        put_data = {'meeting_link': meeting_link,
                    'password': meeting_password,
                    'index_data': index_data,
                    'live_stream': live_stream}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]

        return self.__put(real_url, put_data)

    def meeting_list(self):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'meeting_list'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]

        return self.__get(real_url)

    def meeting_info(self, meeting_id):
        """

        INPUT:
        meeting_id -> meeting ID

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'meeting_info'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]
        real_url = real_url.replace("{meeting_id}", meeting_id)

        return self.__get(real_url)

    def meeting_exists(self, meeting_id):
        """

        INPUT:
        meeting_id -> meeting ID

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'meeting_exists'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['bot']:
            return {'status': 'ERROR', 'statusInfo': 'bot API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['bot'][flavor]
        real_url = real_url.replace("{meeting_id}", meeting_id)

        return self.__get(real_url)

    def queue_media_file_ingestion(self, file_name, workspace_id, recording_title, recording_date, recording_time):

        print(f"loading {file_name}")

        file = open(file_name, 'rb').read()

        ingest_payload = {"title": recording_title,
                          "date": recording_date,
                          "time": recording_time}

        files_payload = {"payload": ("payload", json.dumps(ingest_payload), "application/json", None),
                         "file": (file_name.split("/")[-1],
                                  file, f"{'video/mp4' if file_name.split('.')[-1] in ('mp4', 'webm') else 'audio/mp3'}", None)}

        flavor = 'file'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['ingest']:
            return {'status': 'ERROR', 'statusInfo': 'ingest API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['ingest'][flavor].replace("{workspace_id}", workspace_id)

        print(f"calling {real_url}")

        return self.__multipart_put(real_url, files_payload)

    def workspace_doc_ranked_topic(self, workspace_id, filter_params=None):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_ranked_topic'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        put_data = self.__generate_workspace_filter_params(filter_params)

        return self.__put(real_url, put_data)

    def workspace_doc_ranked_tag(self, workspace_id, filter_params=None):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_ranked_tag'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        put_data = self.__generate_workspace_filter_params(filter_params)

        return self.__put(real_url, put_data)

    def workspace_doc_ranked_speaker(self, workspace_id, filter_params=None):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_ranked_speaker'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        put_data = self.__generate_workspace_filter_params(filter_params)

        return self.__put(real_url, put_data)

    def workspace_doc_exists(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_exists'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_info(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_info'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_transcript(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_transcript'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_summary(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_summary'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_monologues(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_monologues'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_topics(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_topics'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_concepts(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_concepts'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_tags(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_tags'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_metadata_screens(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_metadata_screens'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__get(real_url)

    def workspace_doc_delete(self, workspace_id, doc_id):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_delete'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        real_url = real_url.replace("{doc_id}", doc_id)

        return self.__delete(real_url)

    def workspace_doc_list(self, workspace_id, filter_params=None):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_list'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        put_data = self.__generate_workspace_filter_params(filter_params)

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        return self.__put(real_url, put_data)

    def workspace_doc_search_transcript(self, workspace_id, search_term, filter_params=None):
        """

        INPUT:
        search_term -> search term

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'doc_search_transcript'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        put_data = {'utterance_phrase_match': [search_term]}

        put_data = {}

        if filter_params:
            for filter_tuple in filter_params.items():
                put_data[filter_tuple[0]] = filter_tuple[1]
            
        put_data['utterance_phrase_match'] = [search_term]

        real_url = Hyperia.ENDPOINTS['workspace'][flavor].replace("{workspace_id}", workspace_id)

        return self.__put(real_url, put_data)

    def workspace_public_list(self):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'public_list'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor]

        return self.__get(real_url)


    def workspace_list(self):
        """

        INPUT:

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        flavor = 'list'

        # Make sure this request supports this flavor
        if flavor not in Hyperia.ENDPOINTS['workspace']:
            return {'status': 'ERROR', 'statusInfo': 'workspace API ' + flavor + ' not available'}

        real_url = Hyperia.ENDPOINTS['workspace'][flavor]

        return self.__get(real_url)


    def __multipart_put(self, endpoint, put_data={}):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key
        put_headers = {'apikey': self.apikey}

        # Insert the base url
        put_url = Hyperia.BASE_URL + endpoint

        results = ""
        try:
            results = self.s.put(url=put_url, files=put_data, headers=put_headers)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}

    def __generate_workspace_filter_params(self, filter_params):
        payload_data = {}

        if filter_params is not None:
            allowed_params = ["relative_datetime_range", "date_range", "time_range", "relative_ingest_datetime_range", "ingest_date_range", "speaker_list", "tag_list", "tag_id_list", "label_id_list", "label_id_exclusion_list", "topic_list", "recording_id_list", "utterance_phrase_match", "title_phrase_match", "description_phrase_match", "screen_shared"]

            for key_val in filter_params.keys():
                if key_val not in allowed_params:
                    return {'status': 'ERROR', 'statusInfo': f'invalid parameter: {key_val}'}
                payload_data[key_val] = filter_params[key_val]
        return payload_data

    def __post(self, endpoint, post_data={}):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key
        post_headers = {'apikey': self.apikey}

        # Insert the base url
        post_url = Hyperia.BASE_URL + endpoint

        results = ""
        try:
            results = self.s.post(url=post_url, json=post_data, headers=post_headers)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}

    def __put(self, endpoint, put_data={}):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key
        put_headers = {'apikey': self.apikey}

        # Insert the base url
        put_url = Hyperia.BASE_URL + endpoint

        results = ""
        try:
            results = self.s.put(url=put_url, json=put_data, headers=put_headers)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}

    def __get(self, endpoint):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key
        get_headers = {'apikey': self.apikey}

        # Insert the base url
        get_url = Hyperia.BASE_URL + endpoint

        results = ""
        try:
            results = self.s.get(url=get_url, headers=get_headers)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}

    def __delete(self, endpoint):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key
        del_headers = {'apikey': self.apikey}

        # Insert the base url
        del_url = Hyperia.BASE_URL + endpoint

        results = ""
        try:
            results = self.s.delete(url=del_url, headers=del_headers)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}
