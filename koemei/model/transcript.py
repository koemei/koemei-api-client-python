import json

from koemei.model.base_object import BaseObject
from koemei.utils import check_file_extension
from koemei.utils import settings, log

class Transcript(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Transcript, self).__init__(fields=fields)


    @classmethod
    def get(cls, client, uuid, deleted=False, format='json'):
        url = [settings.get('base', 'paths.api.transcripts'), uuid]
        response = client.request(url=url, accept=format)

        content = None
        if format != 'json':
            content = response
            # always get the json response to build the object
            response = client.request(url=url, accept='json')

        response_json = json.loads(response)
        if content is not None:
            response_json['content'] = content

        return Transcript(fields=response_json)

    @classmethod
    def has_valid_file_extension(cls, file_path):
        return check_file_extension(
            file_path=file_path,
            authorized_file_types=settings.get('base', 'transcript.align.authorized_extensions').split(',')
        )

    @classmethod
    def get_all(cls, client, *args, **kwargs):
        url = [settings.get('base', 'paths.api.transcripts')]

        response = client.request(url=url)
        response_json = json.loads(response)

        transcripts = []

        log.debug(response_json['transcripts'])

        for transcript in response_json['transcripts']:
            transcripts.append(Transcript(fields=transcript))
        return transcripts
