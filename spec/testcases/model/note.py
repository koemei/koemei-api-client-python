import unittest

from koemei.model.note import Note
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings


class NoteTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    def test_init(self):
        fields = {
            'uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
            'media_item_uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
            'parent_uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
        }
        self.model = Note(fields=fields)

        assert hasattr(self.model, 'uuid')
        assert self.model.uuid == fields['uuid']
        assert self.model.media_item_uuid == fields['media_item_uuid']
        assert self.model.parent_uuid == fields['parent_uuid']

    def test_get(self):
        fields = {
            'uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
        }
        self.model = Note.get(client=self.client, uuid=fields['uuid'])
        assert hasattr(self.model, 'uuid') and self.model.uuid == fields['uuid']
        assert hasattr(self.model, 'media_item_uuid') and self.model.media_item_uuid is not None
        assert hasattr(self.model, 'content') and self.model.content is not None
        assert hasattr(self.model, 'start_time') and self.model.start_time is not None
        assert hasattr(self.model, 'type') and self.model.type is not None
        assert hasattr(self.model, 'author') and self.model.author is not None and hasattr(self.author, 'uuid')

    def test_get_all(self):
        self.models = Note.get_all(client=self.client)
        assert len(self.models) > 0
        assert hasattr(self.models[0], 'content')
        assert hasattr(self.models[0], 'uuid')

    def test_create(self):
        """
        Create vanilla note
        """
        pass

    def test_create_highlight(self):
        pass

    def test_create_reply(self):
        pass

    def test_upvote(self):
        pass

    def test_downvote(self):
        pass

if __name__ == "__main__":
    unittest.main()