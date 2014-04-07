import urllib
from koemei.utils.encode import multipart_encode, MultipartParam
from koemei.utils import log, settings, read_file, check_file_extension
from koemei.utils.streaminghttp import register_openers
import json

from base_object import BaseObject
from koemei.model.process import Process

MEDIA_STATUS = {
    'ASR': 1,
    'ALIGN': 2,
    'EDIT': 3,
    'UPLOAD': 4,
    'PUBLISH': 5,
    'TRANSCODE': 6,
    'TSP': 7,
    }

class Media(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Media, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.media'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return Media(fields=response_json["media_item"])

    @classmethod
    def get_all(cls, client, *args, **kwargs):
        url_params = {}
        if kwargs.get('status'):
            url_params.update({'status_filter':  '-'.join(map(lambda x: str(x), kwargs.get('status')))})
        if kwargs.get('search_query'):
            url_params.update({'search_query': kwargs.get('search_query')})

        if kwargs.get('count'):
            url_params.update({'count': kwargs.get('count')})
        if kwargs.get('start'):
            url_params.update({'start': kwargs.get('start')})

        url = [settings.get('base', 'paths.api.media')]

        response = client.request(url=url, url_params=url_params)
        response_json = json.loads(response)

        media = []
        log.debug(response_json['media'])
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
        @param kwargs: title, description, tags, ...
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

        if 'title' in kwargs and kwargs["title"] is not None:
            data.update({
                'title': kwargs.get('title'),
            })

        if 'description' in kwargs:
            data.update({
                'description': kwargs.get('description'),
            })

        # upload from remote url
        if 'http' in media_filename:
            #url.append("?media=" + urllib.quote(media_filename, safe=''))
            #data = "" # should not be empty dict but empty string!
            data.update({
                'media': media_filename
            })
            data, headers_ = multipart_encode(data)

        # upload from local hard drive
        else:
            register_openers()
            data.update(
                {'media': open(media_filename, "rb")}
            )
            data, headers_ = multipart_encode(data)

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

    def transcode(self, client, success_callback_url='', error_callback_url='', **kwargs):
        """
        Transcode an existing media item.
        """
        headers = {}
        url = [settings.get('base', 'paths.api.media'), self.uuid, settings.get('base', 'paths.api.media.transcode')]

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
        log.info("aligning %s" % aligndata)
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

    @property
    def transcription_status(self):
        transcription_status = None

        if hasattr(self, 'processes'):
            transcription_processes = [p for p in self.processes if p.type == Process.st]

        return transcription_status


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