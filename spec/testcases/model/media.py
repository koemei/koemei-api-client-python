import unittest

from koemei.model.media import Media, MEDIA_STATUS
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings


class MediaTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    #def test_init(self):
    #    fields = {
    #        'uuid': '69255493-583c-468c-9962-e5586f494027',
    #    }
    #    self.model = Media(fields=fields)
    #
    #    assert hasattr(self.model, 'uuid')
    #    assert self.model.uuid == fields['uuid']
    #
    #def test_get(self):
    #    """
    #    Create a media and do a get request on it
    #    """
    #    fields = {
    #        'title': 'Test media title',
    #        'description': 'Test media description',
    #        'local_media_file': 'test_64K_short.mp3',
    #    }
    #
    #    media_filename = "%s/%s" % (settings.get('base', 'path.local.media'), fields['local_media_file'])
    #    self.model = Media.create(
    #        client=self.client,
    #        media_filename=media_filename,
    #        title=fields['title'],
    #        description=fields['description'],
    #    )
    #
    #    self.model = Media.get(client=self.client, uuid=self.model.uuid)
    #    assert self.model.title == fields['title']
    #    assert self.model.description == fields['description']
    #
    #def test_get_all(self):
    #    local_media_files = [
    #        'test_mp4_short.mp4',
    #        'test_64K_short.mp3'
    #    ]
    #    for local_media_file in local_media_files:
    #        media_filename = "%s/%s" % (settings.get('base', 'path.local.media'), local_media_file)
    #
    #        self.model = Media.create(
    #            client=self.client,
    #            media_filename=media_filename,
    #        )
    #
    #    self.models = Media.get_all(client=self.client)
    #    assert len(self.models) > 0
    #    assert hasattr(self.models[0], 'title')
    #
    #    # TODO: Test pagination
    #    # TODO: Test filters
    #
    #def test_create_local(self):
    #    local_media_files = [
    #        'test_mp4_short.mp4',
    #        'test_64K_short.mp3'
    #    ]
    #    for local_media_file in local_media_files:
    #        media_filename = "%s/%s" % (settings.get('base', 'path.local.media'), local_media_file)
    #
    #        self.model = Media.create(
    #            client=self.client,
    #            media_filename=media_filename,
    #        )
    #
    #        media_item = Media.get(client=self.client, uuid=self.model.uuid)
    #        assert media_item.uuid == self.model.uuid
    #        assert media_item.title == "%s/%s" % (settings.get('base', 'path.local.media'), local_media_file)
    #        assert media_item.status == MEDIA_STATUS['ASR']
    #        assert media_item.progress == 0
    #
    #def test_create_remote(self):
    #    remote_media_files = [
    #        settings.get('test', 'audio_test_remote_mp3'),
    #        settings.get('test', 'audio_test_remote_youtube'),
    #        settings.get('test', 'audio_test_remote_youtube_https'),
    #    ]
    #
    #    for remote_media_file in remote_media_files:
    #        self.model = Media.create(
    #            client=self.client,
    #            media_filename=remote_media_file,
    #        )
    #        media_item = Media.get(client=self.client, uuid=self.model.uuid)
    #        assert Media.get(client=self.client, uuid=self.model.uuid).uuid == self.model.uuid
    #        assert media_item.title == remote_media_file
    #        assert media_item.status == MEDIA_STATUS['ASR']
    #        assert media_item.progress == 0
    #
    #def test_create_local_metadata(self):
    #    """
    #    Test creation of a media from a local file, by specifying some metadata (title, description, ...)
    #    """
    #    local_media = {
    #        'path': 'test_mp4_short.mp4',
    #        'title': 'Test media title',
    #        'description':'Test media description',
    #    }
    #
    #    media_filename = "%s/%s" % (settings.get('base', 'path.local.media'), local_media['path'])
    #
    #    self.model = Media.create(
    #        client=self.client,
    #        media_filename=media_filename,
    #        title=local_media['title'],
    #        description=local_media['description'],
    #    )
    #
    #    media_item = Media.get(client=self.client, uuid=self.model.uuid)
    #    assert media_item.title == local_media['title']
    #    assert media_item.description == local_media['description']
    #    #TODO: assert creator is owner
    #
    #def test_create_no_transcribe(self):
    #    remote_media_file = settings.get('test', 'audio_test_remote_mp3')
    #    self.model = Media.create(client=self.client, media_filename=remote_media_file, transcribe=False)
    #    media_item = Media.get(client=self.client, uuid=self.model.uuid)
    #    assert Media.get(client=self.client, uuid=self.model.uuid).uuid == self.model.uuid
    #    assert media_item.title == remote_media_file
    #    assert media_item.status in (MEDIA_STATUS['UPLOAD'], MEDIA_STATUS['TRANSCODE'])

    def test_align_local(self):
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

    def test_align_remote(self):
        media_item = Media.create(
            client=self.client,
            media_filename=settings.get('test', 'audio_test_remote_mp3'),
            aligndata="%s/%s" % (settings.get('base', 'path.local.transcripts'), settings.get('test', 'transcript.align')),
            transcribe=False
        )

        assert hasattr(media_item, 'process_alignment')
        assert media_item.process_alignment.status == 'PENDING'
        assert media_item.process_alignment.progress == 0
        assert hasattr(media_item.process_alignment, 'uuid')


    #def test_search_global(self):
    # """
    # Search across all the public videos
    # """
    #    self.models = Media.get_all(client=self.client, search_query=settings.get('test','media.search.query'))
    #    assert len(self.models) > 0
    #    for media_item in self.models:
    #        assert hasattr(self.models[0], 'title')
    #        assert (
    #            settings.get('test','media.search.query') in media_item.title or

    #def test_search_user(self):
    #"""
    #Search across private videos of a user:
    #* if not logged in no private video should be there
    #* if logged in as other user, only protected
    #* if logged in as account owner, display all
    #* check invalid uuid
    #* check public_only
    #"""

    #def test_search_title(self):
    #    """
    #    Check that videos are indexed by title
    #    """
    #    fields = {
    #        'title': 'Test media title',
    #        'description': 'Test media description',
    #        'search_query': 'media title',
    #    }
    #
    #    media_item = Media.create(
    #        client=self.client,
    #        media_filename=settings.get('test', 'audio_test_remote_mp3'),
    #        title=fields['title'])
    #
    #
    #    media = Media.get_all(
    #        client=self.client,
    #        user_uuid=settings.get('credentials', 'koemei_user_uuid'),
    #        search_query=fields['search_query']
    #    )
    #
    #    assert len([m for m in media if m.uuid == media_item.uuid]) > 0

    #def test_search_description(self):
    #def test_search_transcript(self):
    #def test_search_notes(self):
    #def test_search_empty(self):
    #"""
    #Make sure that we get an empty set of videos on incorrect request
    #"""

    #def test_search_too_short_query(self):
    #"""
    #Make sure that we get an httpinvalid error if the search criteria is smaller than 3 characters
    #"""

    #def test_search(self):
    #"""
    #Make sure that search results are ok in the following cases:
    #* multi words
    #* non-utf8 characters
    #* stemming
    #* check case insensitive
    #* check ignore small words ('the', 'and' ...) in multi words requests
    #"""



    """
    def test_metadata(self):
        pass

    def test_delete(self):
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