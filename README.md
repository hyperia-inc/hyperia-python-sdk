# hyperia-python-sdk #

This is a Python SDK for accessing the Hyperia Conversational Intelligence APIs.  With Hyperia, you can quickly build and integrate transcription and conversational intelligence into your application.


## Hyperia ##

Hyperia offers a programmable AI notetaker, real-time streaming call and meeting transcription and NLP analysis, and conversational intelligence as a service.

More information at: https://hyperia.net/



## API Key ##

To use Hyperia, you'll need to obtain an API key and attach that key to all requests. If you do not already have a key, please visit: https://hyperia.net/



## REST API Documentation ##

Hyperia offers dozens of REST API endpoints for doing real-time transcription, leveraging a programmable AI notetaker in Zoom/Google Meet/Teams calls,
or crawling or uploading media for analysis, ingestion, and indexing.  Workspace management, document management, search, and analytics APIs are also
provided.  Full API documentation is available at:

	https://hyperia.net/docs



## Requirements ##

The Python SDK requires that you install the [Requests Python module](http://docs.python-requests.org/en/latest/user/install/#install).

If you are using Hyperia's real-time streaming transcription and NLP analysis functionalities, you will also need to install the 
[Websocket-client Python module](https://github.com/websocket-client/websocket-client#installation).



## Getting Started with the Python SDK ##

To install the Hyperia Python SDK, do the following:

	git clone https://github.com/hyperia-inc/hyperia-python-sdk.git
	cd hyperia-python-sdk
	python setup.py install

Once you have installed the SDK, go to https://hyperia.net/ and register for an API key.  Please create your api_key.txt file with the following command:

	python install_key.py YOUR_API_KEY

Just replace YOUR_API_KEY with your 73 character API key from Hyperia, and you should be good to go.

NOTE: You can also create api_key.txt manually -- just make sure not to include any trailing spaces or linefeeds in the file.  You can validate
the file is the correct size with the command "wc -c api_key.txt" (It should say 73 bytes).



## Streaming Audio for Realtime Transcription and NLP Analysis

You may use the following code sample to stream audio for realtime transcription and NLP analysis:

	python examples/stream_create_and_transcribe.py data/intro_to_ai.pcm

NOTE: Files must be raw PCM, 16000 hz, mono, signed 16 bit integer format.



## Joining Zoom, Google Meet, Or Teams Meetings w/ the Programmable AI Notetaker

You may use the following code sample to have our programmable AI Notetaker join an active meeting:

        <Start a Zoom, Google Meet, or Teams call>

	python meeting_join.py <MEETING_LINK> <MEETING_PASSWORD>



## Ingesting a media file for transcription, computer vision, NLP analysis, and indexing into a searchable Hyperia workspace:

You may use the following code sample to ingest media files into your Hyperia workspace:

	python examples/ingest_video_example.py <FILENAME> <WORKSPACE_ID>

NOTE: Media files can be MP4, MP3, WAV, and other major audio/video formats.



## Using the API to create a workspace, crawl/transcribe/summarize a media file from the web, and perform searches and aggregations in a workspace:

You may use the following code sample to see end-to-end usage of a Hyperia workspace for ingestion,
search, and analytics:

        python examples/e2e_ingest_and_query.py <NAME_FOR_A_NEW_WORKSPACE> <MEDIA_FILE_HTTP_OR_HTTPS_URL> <OPTIONAL: MEDIA_FILE_TITLE>

NOTE: Media files can be MP4, MP3, WAV, and other major audio/video formats.  URLs must be publicly crawlable.


