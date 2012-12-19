php-client
==========

PHP client for Koemei API

A basic use case for generating captions is :

1.  upload media : POST media {media_file_name}
2.  start transcription : POST media/{media_uid}/transcribe
3.  check transcription status (poll) : GET media/{media_uid}/transcribe/{process_uid}
4.  get transcript/captions : GET transcripts/{transcript_uuid}

For a more detailed documentation, please look at https://www.koemei.com/api/
