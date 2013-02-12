Koemei php API client
=====================

*Note : remember to set USERNAME and PASSWORD in the protected variables*

Usage : API.php <method> <accept> <path> [upload] [metadata]

Examples:
*	upload media:		API.php POST text/xml media test.mp3
*	transcribe media:	API.php POST text/xml media/{id}/transcribe
*	transcription status:	API.php GET text/xml media/{id}/transcribe/{process-id}
*	info about media:	API.php GET text/xml media/{id}
