Koemei API python client
=========================

* Note : You need to change the login/pwd in the example or mainAPI. *

Basic use case for generating captions
---------------------

1. Upload a media file

    mainAPI.py -u {audio_file} Media create text/xml

or

    mainAPI.py -u 'http://www.youtube.com/watch?v=xxxxxxxx' Media create text/xml

2. Start transcription

    mainAPI.py -i {media_uuid} Media transcribe text/xml

3. Get transcript/captions

    mainAPI.py -i {uid} Transcript get text/xml

**For a more detailed documentation, please have a look at [the API documentation](https://www.koemei.com/api/)**