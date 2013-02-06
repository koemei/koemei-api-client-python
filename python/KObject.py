
import sys, urllib2

from BaseObject import BaseObject

class KObject(BaseObject):
  def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename="", metadataFilename=""):
      BaseObject.__init__(self, accept, username=username, password=password, uid=uid, process_id=process_id, audioFilename=audioFilename, metadataFilename=metadataFilename)
      self.path = 'kobjects/'

  @BaseObject._reset_headers
  def get(self):
      print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path+self.uid)
      request = urllib2.Request(self.dest+self.path+self.uid, headers=self.headers)
      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def delete(self):
      print >> sys.stderr, 'making delete request to: %s%s' % (self.dest,self.path+self.uid)
      request = urllib2.Request(self.dest+self.path+self.uid, headers=self.headers)
      request.get_method = lambda: 'DELETE'
      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def get_list(self):
      print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path)
      request = urllib2.Request(self.dest+self.path, headers=self.headers)
      BaseObject._execute(self, request)

  # create a new K-Object
  @BaseObject._reset_headers
  def create(self):
      print >> sys.stderr, 'making post request to: %s%s' % (self.dest,self.path)
      self.datagen = {}
      request = urllib2.Request(self.dest+self.path, data="", headers=self.headers)
      BaseObject._execute(self, request)
