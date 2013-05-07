
import sys, urllib2, urllib
from encode import multipart_encode, MultipartParam


def create_metadata(metadataFilename):
    fp = open(metadataFilename,"r")
    metadata = fp.read()
    fp.close()

    return metadata

from BaseObject import BaseObject


class Media(BaseObject):

  def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename="", metadataFilename=""):
      BaseObject.__init__(self, accept, username=username, password=password, uid=uid, process_id=process_id, audioFilename=audioFilename, metadataFilename=metadataFilename)
      self.path = 'media/'
      self.path_trans = '/transcribe'
      self.path_publish = '/publish'
      self.path_unpublish = '/unpublish'

  @BaseObject._reset_headers
  def get(self):
      print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path+self.uid)
      request = urllib2.Request(self.dest+self.path+self.uid, headers=self.headers)
      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def get_list(self):
      print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path)
      request = urllib2.Request(self.dest+self.path, headers=self.headers)
      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def create(self):
      print >> sys.stderr, 'making post request to: %s%s' % (self.dest,self.path)
      self.datagen = {}

      if len(self.audioFilename) > 0:
        if 'http' in self.audioFilename :
            self.path = self.path +"?media="+ urllib.quote(self.audioFilename,safe='')
            self.datagen = "" # should not be empty dict but empty string!
        else :
            if len(self.metadataFilename) > 0:
                self.datagen, headers_ = multipart_encode({ 'metadata' : create_metadata(self.metadataFilename),
                                                         'media' : open(self.audioFilename, "rb") })
            else:
                self.datagen, headers_ = multipart_encode({ 'media' : open(self.audioFilename, "rb") })
            self.headers.update(headers_)

      #print >> sys.stderr, "request headers: ", self.headers

      request = urllib2.Request(self.dest+self.path, data= self.datagen, headers=self.headers)

      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def transcribe(self, success_callback_url=None, error_callback_url=None):
      print >> sys.stderr, 'making post request to: %s%s' % (self.dest,self.path+self.uid+self.path_trans)
      self.datagen = {}

      data = urllib.urlencode({'success_callback_url': success_callback_url, 'error_callback_url': error_callback_url,})
      request = urllib2.Request(self.dest+self.path+self.uid+self.path_trans, data=data, headers=self.headers)
      BaseObject._execute(self, request)


  @BaseObject._reset_headers
  def publish(self):
      print >> sys.stderr, 'making put request to: %s%s' % (self.dest,self.path+self.uid+self.path_publish)
      self.datagen = {}
      request = urllib2.Request(self.dest+self.path+self.uid+self.path_publish, data="", headers=self.headers)
      request.get_method = lambda: 'PUT'
      BaseObject._execute(self, request)

  @BaseObject._reset_headers
  def unpublish(self):
      print >> sys.stderr, 'making put request to: %s%s' % (self.dest,self.path+self.uid+self.path_unpublish)
      self.datagen = {}
      request = urllib2.Request(self.dest+self.path+self.uid+self.path_unpublish, data="", headers=self.headers)
      request.get_method = lambda: 'PUT'
      BaseObject._execute(self, request)