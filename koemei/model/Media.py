import os
import sys
import urllib2
import urllib
from koemei.utils.encode import multipart_encode, MultipartParam
from koemei.utils import log, settings, read_file, check_file_extension
from koemei.utils.streaminghttp import register_openers
import json

from base_object import BaseObject
from koemei.model.process import Process
from koemei.utils.fileprogress import FileProgress


class Media(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Media, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid):
        url = [settings.get('base', 'paths.api.media'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return Media(fields=response_json["media_item"])

    @classmethod
    def get_all(cls, client, *args, **kwargs):
        url_data = {}
        if kwargs.get('status'):
            url_data.update({'status_filter':  '-'.join(map(lambda x: str(x), kwargs.get('status')))})

        url_data = urllib.urlencode(url_data)
        url = [settings.get('base', 'paths.api.media'), url_data]
        response = client.request(url=url)
        response_json = json.loads(response)

        media = []

        for media_item in response_json['media']:
            media.append(Media(fields=media_item))
        return media

    @classmethod
    def create(
        cls,
        client,
        media_filename,
        transcribe=True,
        aligndata=None,
        **kwargs):
        """
        Create a media item.
        If transcript_filename provided: create media and align the transcript.

        @param media_filename: local/remote address of the media file to transcribe
        @param metadata_filename: local path to the metadata file containing media info (title, description, ...)
        @param transcript_filename: local path to the plain text transcript file to align
        @param transcribe: automagically launch transcription
        """

        data = {}
        headers = {}
        headers_ = {}
        url = [settings.get('base', 'paths.api.media')]

        # create the media from a service
        if 'service' in kwargs:
            data.update({
                'service': kwargs.get('service'),
                'item_id': kwargs.get('item_id')}
            )

        # upload from remote url
        if 'http' in media_filename:
            url.append("?media=" + urllib.quote(media_filename, safe=''))
            data = "" # should not be empty dict but empty string!

            if kwargs.get('transcript_filename'):
                data, headers_ = multipart_encode({'transcript': read_file(kwargs.get('transcript_filename')),})

        # upload from local hard drive
        else:
            register_openers()

            # TODO : test this and define metadata file format (json)
            if kwargs.get('metadata_filename'):
                data, headers_ = multipart_encode({
                    'metadata': read_file(kwargs.get('metadata_filename')),
                    'media': open(media_filename, "rb")}
                )
            elif kwargs.get('transcript_filename') is not None:
                data, headers_ = multipart_encode({
                    'transcript': read_file(kwargs.get('transcript_filename')),
                    'media': open(media_filename, "rb")}
                )
            else:
                data, headers_ = multipart_encode({'media': open(media_filename, "rb")})

        headers.update(headers_)
        response = client.request(url=url, data=data, headers=headers)
        response_json = json.loads(response)
        media_item = Media(fields=response_json['media_item'])
        if aligndata is not None:
            media_item.align(client=client, aligndata=aligndata)
        elif transcribe:
            media_item.transcribe(client=client)

        return media_item

    def transcribe(self, client, success_callback_url='', error_callback_url='', **kwargs):
        """
        Transcribe an existing media item.
        """
        headers = {}
        url = [settings.get('base', 'paths.api.media'), self.uuid, settings.get('base', 'paths.api.media.transcribe')]

        data = urllib.urlencode(
            {'success_callback_url': success_callback_url, 'error_callback_url': error_callback_url})

        response = client.request(url=url, data="", headers=headers)
        response_json = json.loads(response)
        self.process_transcription = Process(fields=response_json['process'])
        return self.process_transcription

    def align(self, client, aligndata, success_callback_url='', error_callback_url='', **kwargs):
        """
        Align an existing media item.
        """
        data = {}
        headers = {}
        headers_ = {}

        url = [settings.get('base', 'paths.api.media'), self.uuid, settings.get('base', 'paths.api.media.align')]

        data, headers_ = multipart_encode({
            'aligndata': read_file(aligndata),
            'success_callback_url': success_callback_url,
            'error_callback_url': error_callback_url
            })
        headers.update(headers_)
        response = client.request(url=url, data=data, headers=headers)
        response_json = json.loads(response)
        self.process_alignment = Process(fields=response_json['process'])
        return self.process_alignment

    @classmethod
    def has_valid_file_extension(cls, file_path):
        return check_file_extension(
            file_path=file_path,
            authorized_file_types=settings.get('base', 'media.authorized_extensions').split(',')
        )


"""
    @BaseObject._reset_headers
    def publish(self):
        print >> sys.stderr, 'making put request to: %s%s' % (self.dest, self.path + self.uid + self.path_publish)

        data = {}
        if self.service:
            data.update({'service_name': self.service,})

        data = urllib.urlencode(data)
        url = "%s/%s/%s/%s?%s" % (self.dest, self.path, self.uid, self.path_publish, data)

        request = urllib2.Request(url, data="", headers=self.headers)
        request.get_method = lambda: 'PUT'
        BaseObject._execute(self, request)

    @BaseObject._reset_headers
    def unpublish(self):
        print >> sys.stderr, 'making put request to: %s%s' % (self.dest, self.path + self.uid + self.path_unpublish)
        request = urllib2.Request(self.dest + self.path + self.uid + self.path_unpublish, data="", headers=self.headers)
        request.get_method = lambda: 'PUT'
        BaseObject._execute(self, request)

    def delete(self):
        #TODO
        pass

"""