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

    def test_get_json(self):
        self.model = Transcript.get_all(self.client)[0]
        transcript = Transcript.get(self.client, uuid=self.model.uuid)

        assert hasattr(transcript, 'segmentation')
        assert len(transcript.segmentation) > 0
        # TODO: from jsonschema import validate
        for segment in transcript.segmentation:
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

    def test_get_srt(self):
        self.model = Transcript.get_all(self.client)[0]
        transcript = Transcript.get(self.client, uuid=self.model.uuid, format='srt')
        assert hasattr(transcript, 'content')
        assert '00:00:00,000 -->' in transcript.content
        # TODO: do moe thorough validation (see https://github.com/riobard/srt.py/blob/master/srt.py for a nice parser)

    def test_get_all(self):
        self.models = Transcript.get_all(client=self.client)
        assert len(self.models) > 0
        assert hasattr(self.models[0], 'uuid')
        assert hasattr(self.models[0], 'version')



if __name__ == "__main__":
    unittest.main()