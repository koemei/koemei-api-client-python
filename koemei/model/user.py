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


class User(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(User, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.users'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return User(fields=response_json["user"])