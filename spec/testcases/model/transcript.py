import unittest

from koemei.model.transcript import Transcript
from koemei.client import KoemeiClient
from koemei.utils import read_settings_file, log, settings


class TranscriptTestCase(unittest.TestCase):

    def setUp(self):
        self.client = KoemeiClient()

    def tearDown(self):
        self.model = None
        self.models = None
        self.client = None

    def test_init(self):
        fields = {
            'uuid': '8d40175d-274b-4885-8ad3-c256054cb024',
        }
        self.model = Transcript(fields=fields)

        assert hasattr(self.model, 'uuid')
        assert self.model.uuid == fields['uuid']

    def test_get(self):
        fields = {
            'uuid': '8d40175d-274b-4885-8ad3-c256054cb024',
        }
        self.model = Transcript.get(client=self.client, uuid=fields['uuid'])
        assert hasattr(self.model, 'segmentation')
        assert len(self.model.segmentation) > 0
        # TODO: from jsonschema import validate
        for segment in self.model.segmentation:
            print segment
            assert 'start' in segment
            assert 'end' in segment
            #assert 'speaker' in segment
            assert 'labels' in segment
            assert len(segment['labels']) > 0
            for label in segment['labels']:
                assert 'start' in label
                assert 'end' in label
                assert 'confidence' in label
                #assert 'id' in label
                assert 'value' in label


if __name__ == "__main__":
    unittest.main()