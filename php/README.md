Koemei php API client
=====================

*Note : remember to set USERNAME and PASSWORD in the protected variables*

Examples:
*	upload media:		API.php POST media text/xml test.mp3
*	transcribe media:	API.php POST media text/xml media/{id}/transcribe
*	transcription status:	API.php GET text/xml media/{id}/transcribe/{process-id}
*	info about media:	API.php GET text/xml media/{id}
