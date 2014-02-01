import unittest

from koemei.model.media import Media
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings


class MediaTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    def test_init(self):
        fields = {
            'uuid': '69255493-583c-468c-9962-e5586f494027',
        }
        self.model = Media(fields=fields)

        assert hasattr(self.model, 'uuid')
        assert self.model.uuid == fields['uuid']

    def test_get(self):
        fields = {
            'uuid': '69255493-583c-468c-9962-e5586f494027',
        }
        self.model = Media.get(client=self.client, uuid=fields['uuid'])
        assert hasattr(self.model, 'title') and self.model.title is not None
        assert self.model.uuid == fields['uuid']


    def test_get_all(self):
        self.models = Media.get_all(client=self.client)
        assert len(self.models) > 0
        assert hasattr(self.models[0], 'title')

        # TODO: Test pagination

    def test_create_local(self):
        local_media_files = [
            'test_mp4_short.mp4',
            'test_64K_short.mp3'
        ]
        for local_media_file in local_media_files:
            media_filename = "%s/%s" % (settings.get('base', 'path.local.media'), local_media_file)

            self.model = Media.create(client=self.client, media_filename=media_filename)

            media_item = Media.get(client=self.client, uuid=self.model.uuid)
            assert media_item.uuid == self.model.uuid
            assert media_item.title == "%s/%s" % (settings.get('base', 'path.local.media'), local_media_file)
            assert hasattr(media_item, 'process_transcription')
            assert media_item.process_transcription.status == 'PENDING'
            assert media_item.process_transcription.progress == 0
            assert hasattr(media_item.process_transcription, 'uuid')

    def test_create_remote(self):
        remote_media_files = [
            settings.get('test', 'audio_test_remote_mp3'),
            settings.get('test', 'audio_test_remote_youtube'),
            settings.get('test', 'audio_test_remote_youtube_https'),
        ]

        for remote_media_file in remote_media_files:
            self.model = Media.create(client=self.client, media_filename=remote_media_file)
            media_item = Media.get(client=self.client, uuid=self.model.uuid)
            assert Media.get(client=self.client, uuid=self.model.uuid).uuid == self.model.uuid
            assert media_item.title == remote_media_file
            assert hasattr(media_item, 'process_transcription')
            assert media_item.process_transcription.status == 'PENDING'
            assert media_item.process_transcription.progress == 0
            assert hasattr(media_item.process_transcription, 'uuid')

    def test_create_no_transcribe(self):
            remote_media_file = settings.get('test', 'audio_test_remote_mp3')
            self.model = Media.create(client=self.client, media_filename=remote_media_file, transcribe=False)
            media_item = Media.get(client=self.client, uuid=self.model.uuid)
            assert Media.get(client=self.client, uuid=self.model.uuid).uuid == self.model.uuid
            assert media_item.title == remote_media_file
            assert not hasattr(media_item, 'process_transcription')

    def test_transcribe(self):
        media_item = Media.create(client=self.client, media_filename="%s/%s" % (settings.get('base', 'path.local.media'), 'test_mp4_short.mp4'))
        assert hasattr(media_item, 'process_transcription')
        assert media_item.process_transcription.status == 'PENDING'
        assert media_item.process_transcription.progress == 0
        assert hasattr(media_item.process_transcription, 'uuid')

    def test_align(self):
        media_item = Media.create(
            client=self.client,
            media_filename="%s/%s" % (settings.get('base', 'path.local.media'), 'test_mp4_short.mp4'),
            aligndata="%s/%s" % (settings.get('base', 'path.local.transcripts'), settings.get('test', 'transcript.align')),
            transcribe=False
        )

        assert hasattr(media_item, 'process_alignment')
        assert media_item.process_alignment.status == 'PENDING'
        assert media_item.process_alignment.progress == 0
        assert hasattr(media_item.process_alignment, 'uuid')

    """
    def test_search(self):
        self.models = Media.get_all(client=self.client, search_query=settings.get('test','media.search.query'))
        assert len(self.models) > 0
        for media_item in self.models:
            assert hasattr(self.models[0], 'title')
            assert (
                settings.get('test','media.search.query') in media_item.title or
    """

    """
    def test_metadata(self):
        pass

    def test_quota(self):
        pass

    def test_callbacks(self):
        pass

    def test_publish(self):
        pass

    def test_unpublish(self):
        pass
    """

if __name__ == "__main__":
    unittest.main()