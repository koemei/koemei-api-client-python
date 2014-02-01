import unittest

from koemei.model.user import User
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    def test_init(self):
        fields = {
            'uuid': '69255493-583c-468c-9962-e5586f494027',
            'uuid': 'testuser@koemei.com',
        }
        self.model = User(fields=fields)

        assert hasattr(self.model, 'uuid')
        assert self.model.uuid == fields['uuid']
        assert hasattr(self.model, 'email')
        assert self.model.uuid == fields['uuid']

    def test_get(self):
        fields = {
            'uuid': '69255493-583c-468c-9962-e5586f494027',
        }
        self.model = Media.get(client=self.client, uuid=fields['uuid'])
        assert hasattr(self.model, 'title') and self.model.title is not None
        assert self.model.uuid == fields['uuid']

    """
    def test_create(self):
        pass

    def test_login(self):
        pass

    def test_quota(self):
        pass
    """

if __name__ == "__main__":
    unittest.main()