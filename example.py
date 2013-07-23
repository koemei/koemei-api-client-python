#!/usr/bin/python
# ==============================================================
#  (c) 2010 Koemei SA
#  Author: Marina Zimmermann.

# ==============================================================
# EXAMPLE USAGE:
# 1) Upload a media file
# 2) Request a transcript
# 3) Save transcript
#    (can also be done separately using the Transcript object)
# 4) Publish transcript (will be made available to the public)
# 5) Unpublish transcript
# ==============================================================

import sys
import re
import time
from Media import Media

# for streaming
from streaminghttp import register_openers

username = "<changeme>"
password = "<changeme>"

def main():
    register_openers()
    upload_transcribe(audioFilename="test.mp3")
    #upload_align(audioFilename="test.mp3", transcriptFilename="transcript_to_align.txt")
    #publish_unpublish(media_uuid='682bd899-14fd-4db4-bd53-badc346e789c')


def upload_transcribe(audioFilename):
    """
    Upload a media file to Koemei for transcription
    """

    # 1) Upload a media file
    inst = Media(accept="text/xml", username=username, password=password, audioFilename=audioFilename)
    inst.create()

    # extract the uid given to this media item
    if inst.response.code == 200:
        print "Media item has been created successfully"
        search = None
        search = re.search("<id>(.*)</id>", inst.response.read())
        if search is not None:
            uid = str(search.group(1))
            print "The following uid has been extracted: %s" % uid
        else:
            print >> sys.stderr, "An error occured trying to extract the uid"

    else:
        print >> sys.stderr, "-------- An error occurred, response: --------"
        print >> sys.stderr, inst.response.code, inst.response.msg
        print >> sys.stderr, "-------- Headers --------"
        print >> sys.stderr, inst.response.headers

    inst.uid = uid

    # 2) Request a transcript of the just uploaded media item
    # you should change those 2 callbacks to the url of a handler callback on your website
    inst.transcribe(success_callback_url=None, error_callback_url=None)

    # extract the process id given to this process:
    if inst.response.code == 202:
        print "Transcription has been accepted"
        search = None
        search = re.search(
            '<atom:link href="https://www.koemei.com/REST/media/.*/transcribe/(.*)" rel="self"></atom:link>',
            inst.response.read())
        if search is not None:
            process_id = search.group(1)
            print "The following process id has been extracted: %s" % process_id
        else:
            print >> sys.stderr, "An error occurred trying to extract the process id"

    else:
        print >> sys.stderr, "-------- An error occurred, response: --------"
        print >> sys.stderr, inst.response.code, inst.response.msg
        print >> sys.stderr, "-------- Headers --------"
        print >> sys.stderr, inst.response.headers


def publish_unpublish(media_uuid):
    """
    Publish and unpublish a media item's transcript.
    Publishing a transcript will make it available to anyone that knowns its uuid
    """
    media_item = Media(accept='text/xml', username=username, password=password, uid=media_uuid)
    media_item.get()
    #from xml.dom import minidom
    #xmldoc = minidom.parseString(media_item.response.read())
    # current_transcript_uuid = xmldoc.getElementsByTagName('currentTranscript')[0].getElementsByTagName('id')[0].firstChild.data
    media_item.publish()
    #media_item.unpublish()


def upload_align(audioFilename, transcriptFilename):
    """
    Upload a media file to Koemei for alignment
    NOTE : you will need your account to be setup to use this feature
    """

    # 1) Upload a media file
    inst = Media(accept="text/xml", username=username, password=password, audioFilename=audioFilename, transcriptFilename=transcriptFilename)
    inst.create()

    # extract the uid given to this media item
    if inst.response.code == 200:
        print "Media item has been created successfully"
        search = None
        search = re.search("<id>(.*)</id>", inst.response.read())
        if search is not None:
            uid = str(search.group(1))
            print "The following uid has been extracted: %s" % uid
        else:
            print >> sys.stderr, "An error occured trying to extract the uid"

    else:
        print >> sys.stderr, "-------- An error occurred, response: --------"
        print >> sys.stderr, inst.response.code, inst.response.msg
        print >> sys.stderr, "-------- Headers --------"
        print >> sys.stderr, inst.response.headers

    inst.uid = uid

if __name__ == "__main__":
    main()
