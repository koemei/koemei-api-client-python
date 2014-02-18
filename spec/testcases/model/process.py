import unittest

from koemei.model.process import Process
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings


class ProcessTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    def test_init(self):
        fields = {
            'uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
        }
        self.model = Process(fields=fields)

        assert hasattr(self.model, 'uuid')
        assert self.model.uuid == fields['uuid']

    def test_get(self):
        fields = {
            'uuid': '81c7ed5a-0c21-4485-af81-56a46921dff9',
        }
        self.model = Process.get(client=self.client, uuid=fields['uuid'])
        assert hasattr(self.model, 'status') and self.model.status is not None
        assert self.model.uuid == fields['uuid']
        assert hasattr(self.model, 'status')

    def test_get_all(self):
        self.models = Process.get_all(client=self.client)
        assert len(self.models) > 0
        assert hasattr(self.models[0], 'status')


if __name__ == "__main__":
    unittest.main()