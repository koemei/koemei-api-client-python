from koemei.model.base_object import BaseObject
from koemei.utils import check_file_extension

class Transcript(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Transcript, self).__init__(fields=fields)
        self.path = 'transcripts/'

    """
    @BaseObject._reset_headers
    def get(self):
        print >> sys.stderr, 'making get request to: %s%s' % (self.dest, self.path + self.uid)
        request = urllib2.Request(self.dest + self.path + self.uid, headers=self.headers)
        BaseObject._execute(self, request)

    @BaseObject._reset_headers
    def get_list(self):
        print >> sys.stderr, 'making get request to: %s%s' % (self.dest, self.path)

        data = {}

        if self.count:
            data.update({'count': self.count})

        if self.status:
            data.update({'status_filter': '-'.join(map(lambda x: str(x), self.status))})

        data = urllib.urlencode(data)
        url = "%s/%s?%s" % (self.dest, self.path, data)

        request = urllib2.Request(url, headers=self.headers)
        BaseObject._execute(self, request)
    """

    @classmethod
    def has_valid_file_extension(cls, file_path):
        return check_file_extension(
            file_path=file_path,
            authorized_file_types=settings.get('base', 'transcript.align.authorized_extensions').split(',')
        )
