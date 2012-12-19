Koemei API python client
=========================

*Note : You need to change the login/pwd on line 50.*

*   To make an upload:

API.py POST text/xml  media {audio_file}

or

API.py POST text/xml media http://www.youtube.com/watch?v=xxxxxxxx

*   To start transcription

API.py  POST text/xml  media/{media_UUID}/transcribe

*   To check status:

API.py GET text/xml media/{media_UUID}/transcribe/{process_UUID}

*   To get the transcript:

API GET text/xml transcripts/{transcript_UUID}

*   To list your uploads:

API GET text/xml media

*   To delete a media

API DELETE text/xml kobjects/{kobject_UUID}

*   To create a new empty K-Object :

API.py POST text/xml kobjects

*   To upload a media to a K-Object :

API.py  POST text/xml  kobjects/{kobject_UUID}/media {audio file}
