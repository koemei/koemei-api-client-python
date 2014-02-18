Koemei API python client
=========================

Installation
------------

1. Install

```
python setup.py install
```

2. Copy settings.example.ini to settings.ini and fill in your credentials and configuration options.


Basic use case for generating captions
---------------------

** See the `scripts` folder for examples **

1. Upload a media file

    mainAPI.py -u {audio_file} Media create text/xml

or

    mainAPI.py -u 'http://www.youtube.com/watch?v=xxxxxxxx' Media create text/xml

2. Start transcription

    mainAPI.py -i {media_uuid} Media transcribe text/xml

3. Get transcript/captions

    mainAPI.py -i {uid} Transcript get text/xml

**For a more detailed documentation, please have a look at [the API documentation](https://www.koemei.com/api/)**



Known issues
---------

* Automatic alignment may break with some non-ascii characters. To find those: find non ascii chars: perl -ne 'print "$. $_" if m/[\x80-\xFF]/'  utf8.txt

Troubleshooting
----------

Soon!

Next steps
----------

* More testing
