
import sys, urllib2

from BaseObject import BaseObject

class Process(BaseObject):
  def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename="", metadataFilename=""):
      BaseObject.__init__(self, accept, username=username, password=password, uid=uid, process_id=process_id, audioFilename=audioFilename, metadataFilename=metadataFilename)
      self.path = 'media/'

  @BaseObject._reset_headers
  def get(self):
      print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path+self.uid+self.path_trans+self.process_id)
      request = urllib2.Request(self.dest+self.path+self.uid+self.path_trans+self.process_id, headers=self.headers)
      BaseObject._execute(self, request)

