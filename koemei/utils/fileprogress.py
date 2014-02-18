import os, urllib2
from progressbar import *

class FileProgress(file):
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker(),left='[',right=']'),
           ' ', ETA(), ' ', FileTransferSpeed()]

    def __init__(self, path, mode):
        file.__init__(self, path, mode)
        self.seek(0, os.SEEK_END)
        self._total = self.tell()
        self.seek(0)

        self._seen = 0.0
        self._pbar = ProgressBar(widgets=self.widgets, maxval=100)
        self._pbar.start() 

    def __len__(self):
        return self._total

    def read(self, size):
        data = file.read(self, size)
        self.update(len(data))
        return data

    def close(self):
        file.close(self)
        self._pbar.finish()

    def update(self, size):
        self._seen += size
        pct = (self._seen / self._total) * 100.0
        self._pbar.update(pct)
