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
import os
import traceback
from koemei.model.media import Media
from koemei.model.transcript import Transcript
from koemei.client import KoemeiClient
from koemei.utils import settings, log
from koemei.utils.file import csv_to_json

# for streaming
from koemei.utils.streaminghttp import register_openers

client = KoemeiClient()

def main():
    """
    # transcribe one file
    upload_transcribe(media_filename="%s/%s" % (settings.get('base', 'path.local.media'), 'test_mp4_short.mp4'))

    # transcribe all files located in local folder
    for f in os.listdir(settings.get('base', 'path.local.media')):
        if Media.has_valid_file_extension(f):
            upload_transcribe(media_filename="%s/%s" % (settings.get('base', 'path.local.media'), f))
        else:
            log.debug("Skipped media file %s" % f)

    # transcribe all files located in a csv file (http links)
    media_urls = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.transcribe.csv')
        )
    )['data']
    for media_path in media_urls:
        upload_transcribe(media_filename=media_path[0])

    upload_align(
        media_filename="%s/%s" % (settings.get('base', 'path.local.media'), 'test_mp4_short.mp4'),
        aligndata="%s/%s" % (settings.get('base', 'path.local.transcripts'), settings.get('test', 'transcript.align')),
    )


    """

    #batch_download_transcript()
    #batch_upload_transcribe()
    #batch_align()
    #batch_transcribe()
    batch_anthrotranscribe()



def batch_download_transcript():
    register_openers()

    media_to_download_transcript_for = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.transcripts'),
            settings.get('test', 'media.download_transcript.csv')
        )
    )['data']
    for media_item in media_to_download_transcript_for:
        download_transcript(
            media_uuid=media_item[0]
        )


def batch_upload_transcribe():
    register_openers()

    media_to_upload_transcribe = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.transcribe.csv')
        )
    )['data']
    for media_item in media_to_upload_transcribe:
        upload_transcribe(
            media_filename=media_item[0].strip(),
            title=media_item[1]
        )


def download_transcript(media_uuid):
    media_item = Media.get(client=client, uuid=media_uuid)
    print media_item.current_transcript

    transcript = Transcript.get(client=client, uuid=media_item.current_transcript['uuid'], format='json')
    if not os.path.exists(settings.get('base','path.local.scripts.output')):
        os.makedirs(settings.get('base','path.local.scripts.output'))
    f = open("%s/%s.srt" % (settings.get('base','path.local.scripts.output'), media_item.title), 'w')
    f.write(transcript.content)


def batch_align():
    register_openers()

    # align all the files from the csv
    media_to_align = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.align.csv')
        )
    )['data']
    for media_item in media_to_align:
        upload_align(
            media_filename=media_item[1].strip(),
            aligndata="%s/%s.txt" % (
                settings.get('base', 'path.local.transcripts'),
                media_item[0],
            )
        )


def batch_transcribe():
    register_openers()

    # transcribe all the files from the csv
    media_to_transcribe = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.existing.transcribe.csv')
        )
    )['data']
    for media_item in media_to_transcribe:
        transcribe(
            media_uuid=media_item[0],
        )

def batch_anthrotranscribe():
    register_openers()

    # transcribe all the files from the csv
    media_to_anthrotranscribe = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.existing.anthrotranscribe.csv')
        )
    )['data']
    for media_item in media_to_anthrotranscribe:
        anthrotranscribe(
            media_uuid=media_item[0],
        )


def upload_transcribe(media_filename, title=None):
    """
    Upload a media file to Koemei for transcription
    """

    try:
        log.info("Upload and transcribe file %s ..." % media_filename)
        media_item = Media.create(
            client=client,
            media_filename=media_filename,
            title=title
        )
        log.info("... OK - media uuid: %s" % media_item.uuid)
    except Exception, e:
        log.error("... Error creating media %s ..." % media_filename)
        log.error(e)
        log.error(traceback.format_exc())
        raise e


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


def upload_align(media_filename, aligndata):
    """
    Upload a media file to Koemei for alignment
    NOTE : you will need your account to be specially setup to use this feature
    """

    try:
        log.info("Upload and align media %s ..." % media_filename)

        media_item = Media.create(
            client=client,
            media_filename=media_filename,
            aligndata=aligndata,
            transcribe=False
        )

        log.info("... OK - media uuid: %s" % media_item.uuid)
    except Exception, e:
        log.error("... Error aligning media %s ..." % media_filename)
        log.error(e)
        log.error(traceback.format_exc())
        raise e

def transcribe(media_uuid):
    """
    Launch transcription process for a given media
    """
    media_item = Media.get(client=client, uuid=media_uuid)
    media_item.transcribe(client=client)


def anthrotranscribe(media_uuid):
    """
    Launch transcription process for a given media
    """
    media_item = Media.get(client=client, uuid=media_uuid)
    media_item.anthrotranscribe(client=client)


if __name__ == "__main__":
    main()