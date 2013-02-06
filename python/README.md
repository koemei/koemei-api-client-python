Koemei API python client
=========================

*Note : You need to change the login/pwd in the example or mainAPI.*

*Instructions for using the command line with mainAPI.py*

*   To make an upload:

mainAPI.py -u {audio_file} Media create text/xml

or

mainAPI.py -u http://www.youtube.com/watch?v=xxxxxxxx Media create text/xml

*   To start transcription

mainAPI.py -i {uid} Media transcribe text/xml

*   To check status:

mainAPI.py -i {uid} -p {process_id}  Process get text/xml

*   To get the transcript:

mainAPI.py -i {uid} Transcript get text/xml

*   To list your uploads:

mainAPI.py Media get_list text/xml

*   To delete a media

mainAPI.py -i {uid} KObject delete text/xml

*   To create a new empty K-Object :

mainAPI.py KObject create text/xml

*An example of the direct use of the classes is found in example.py*

*   Upload a media file

*   Request a transcript

*   Check progress of transcription repeatedly (might take very long and is not necessarily recommended)

*   Save transcript (can also be done separately using the Transcript object)
