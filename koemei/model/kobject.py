import urllib
from koemei.utils.encode import multipart_encode, MultipartParam
from koemei.utils import log, settings, read_file, check_file_extension
from koemei.utils.streaminghttp import register_openers
import json

from base_object import BaseObject


class KObject(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(KObject, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.kobjects'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return KObject(fields=response_json["kobject"])

    @classmethod
    def delete(cls, client, uuid, **kwargs):
        url_params = {}
        if kwargs.get('delete_transcripts'):
            url_params.update({'delete_transcripts': 'true'})
        if kwargs.get('delete_storage'):
            url_params.update({'delete_storage': 'true'})

        url = [settings.get('base', 'paths.api.kobjects'), uuid]
        response = client.request(url=url, url_params=url_params, method='DELETE')
        print
        print response
        print
        response_json = json.loads(response)
        return KObject(fields=response_json['kobject'])
