import json

from koemei.model.base_object import BaseObject
from koemei.utils import check_file_extension
from koemei.utils import settings


class Transcript(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Transcript, self).__init__(fields=fields)


    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.transcripts'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return Transcript(fields=response_json)

    @classmethod
    def has_valid_file_extension(cls, file_path):
        return check_file_extension(
            file_path=file_path,
            authorized_file_types=settings.get('base', 'transcript.align.authorized_extensions').split(',')
        )
