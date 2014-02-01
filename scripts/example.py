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

    # align all the
    media_to_align = csv_to_json(
        csv_filename="%s/%s" % (
            settings.get('base', 'path.local.media'),
            settings.get('test', 'media.align.csv')
        )
    )['data']
    for media_item in media_to_align:
        upload_align(
            media_filename=media_item[1],
            aligndata="%s/%s.txt" % (
                settings.get('base', 'path.local.transcripts'),
                media_item[0],
            )
        )

    """to_align = [
        #('99abd21f-237d-4575-921b-67cdfe456f69','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-09-27/bc34ed09-fd1e-4831-b202-d0c93b4c496e/99abd21f-237d-4575-921b-67cdfe456f69.media?Signature=udmDmTy5YDzk3VzhYZ4KwmB7YPU%3D&Expires=1386205690&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('74daa8c4-4a07-4043-8632-654cba58eaa0','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/f0300e1d-2eeb-4e16-9003-1d9dd0a68e32/74daa8c4-4a07-4043-8632-654cba58eaa0.media?Signature=Tkq0rWMxe7Kdu%2FEhl5C%2B1LUfNCU%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('cf19a0a6-7dba-4d27-a20a-68f307d1765d','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/1f3d3717-b3a1-4fa7-a433-b47a0d82c2ef/cf19a0a6-7dba-4d27-a20a-68f307d1765d.media?Signature=CnPXV2z6Q9lcDOU69ZnHR%2FrAt3c%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('527e01c7-39bb-4f65-ad2c-4ff6a142f125','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/e880a69a-6feb-4ef8-b51f-9f09b4fd726b/527e01c7-39bb-4f65-ad2c-4ff6a142f125.media?Signature=6eFIP76z6cF8AiuwXrhACssPylA%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('80731283-b1dc-4baa-ac1d-e76f6756aa59','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/d760a046-e2c4-4f3e-9e8f-1551be630989/80731283-b1dc-4baa-ac1d-e76f6756aa59.media?Signature=IbCkSoc0ezz6RXNPOFX8V%2BwRzKA%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('d52c414f-f2c6-4465-9bdf-91cd73fd2a90','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/92158a74-c646-4383-b188-d73093599886/d52c414f-f2c6-4465-9bdf-91cd73fd2a90.media?Signature=zfrRJM4XZDeQvwiDrX2PLQTCRiE%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('53217b0e-f0d1-4f3a-9d94-620f399c4de3','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/d719d8b1-c2b7-4b3e-a600-9295f30fb60a/53217b0e-f0d1-4f3a-9d94-620f399c4de3.media?Signature=gaPFNC01D%2Ftxcx%2BnDbESJopQUYc%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('e2d79ca6-c3df-4ed1-b200-fca2dd38c081','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/60a6c68b-56d1-4867-9eaa-2c59d997c924/e2d79ca6-c3df-4ed1-b200-fca2dd38c081.media?Signature=CfBPgF%2FkE2CLMif28Tw43YYILqs%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('08f50202-e7f4-4afa-9e93-a43fcbc911c9','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/68152cd0-6019-4d9e-963a-b72efa4de7cc/08f50202-e7f4-4afa-9e93-a43fcbc911c9.media?Signature=9RMM8zrqcu79uDWvZPRGGk3GoxY%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('f5012896-b71e-44d4-840c-b39935d479f2','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/0fc7eb38-dc4b-4a94-8b09-33df26003104/f5012896-b71e-44d4-840c-b39935d479f2.media?Signature=%2FV3tgJ5oKjmn6z1lMw%2FTjxvb2Gw%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('735c248e-765a-4265-9eaf-0b781f36e032','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/f84e0690-2413-440d-9690-a38cd6ce5ddd/735c248e-765a-4265-9eaf-0b781f36e032.media?Signature=h1I9fEjUMNAAWWBy66dp2QmLovY%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('266da481-3acf-42dc-96cc-313ad2fab2e4','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/c392380c-0525-4ee4-8c08-86d1fcd7808f/266da481-3acf-42dc-96cc-313ad2fab2e4.media?Signature=ZO%2FzOeFdMjzVFMKA1fZj9XSLaaQ%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('7942ff9d-1414-414e-bb9d-28ea8af18ef9','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/80e3c9ad-69f7-4b69-b37e-79b169a7b901/7942ff9d-1414-414e-bb9d-28ea8af18ef9.media?Signature=I0%2BchNQ8aW6LoXGjN3JLoOCK09I%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
        ('5d43e6b7-454d-4d79-b805-ba476222e00d','https://usermedia.koemei.com.s3.amazonaws.com/60cc6ae9-0adf-45b0-a186-796f515896c4/399de12f-bef7-41a7-b9fd-5b35c1bc4d9b/13-12-04/1653263e-78f0-40de-9af5-a19161f27ee1/5d43e6b7-454d-4d79-b805-ba476222e00d.media?Signature=cLfe3UraQkX4pYhcmBfZDjF2TfI%3D&Expires=1388847043&AWSAccessKeyId=AKIAI6JK3RXCKBQ54KXA'),
    ]
    for uuid,url in to_align:
        print "sending %s" % uuid
        local_align_path = "tmp/alignment/%s.txt" % uuid
        if os.path.exists(local_align_path):
            upload_align(audioFilename=url, transcriptFilename=local_align_path)
        else:
            print "Error file %s not present" % local_align_path
    """


    #upload_align(
    #    audioFilename="https://s3.amazonaws.com/tmp.koemei.com/CS169_v13_w6l2s8.mp4",
    #    transcriptFilename="alignment/CS169_v13_w6l2s8.txt")
    #publish_unpublish(media_uuid='682bd899-14fd-4db4-bd53-badc346e789c')


def upload_transcribe(media_filename):
    """
    Upload a media file to Koemei for transcription
    """

    try:
        log.info("Upload and transcribe file %s ..." % media_filename)
        media_item = Media.create(client=client, media_filename=media_filename)
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
        log.info("Upload and align file %s ..." % media_filename)
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


if __name__ == "__main__":
    main()