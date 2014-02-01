from koemei.utils import log, settings, read_file
import json

from base_object import BaseObject


class Process(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Process, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.processes'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return Process(fields=response_json["process"])

    @classmethod
    def get_all(cls, client, *args, **kwargs):
        url = [settings.get('base', 'paths.api.processes')]
        response = client.request(url=url)
        response_json = json.loads(response)

        processes = []

        for process in response_json['processes']:
            processes.append(Process(fields=process))
        return processes