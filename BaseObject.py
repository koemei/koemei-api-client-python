
import sys, urllib2

class NotImplemented(Exception):
  def __init__(self, expr, msg):
      self.expr = expr
      self.msg = msg

class BaseObject:
  def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename="", metadataFilename=""):
      self.accept = accept
      self.username = username
      self.password = password
      self.path = ''
      self.path_trans = "/transcribe/"
      self.uid = uid
      self.process_id = process_id
      self.audioFilename = audioFilename
      self.metadataFilename = metadataFilename
      self.datagen = {}
      self.headers = {}
      self.dest = 'https://www.koemei.com/REST/'
      self.response = {}

  @classmethod
  def _reset_headers(cls, func):
      def new_func(self):
          self.headers = {}
          import base64
          if self.username != "" and self.password != "":
             auth_string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
             self.headers.update( { 'authorization': 'basic %s' % auth_string,
                            'accept' : self.accept,})
          else:
             print >> sys.stderr, 'The username and/or password are empty.'
             exit()

          func(self)

      return new_func


  def create(self):
      raise NotImplemented('create', 'This action is not implemented')

  def delete(self):
      raise NotImplemented('delete', 'This action is not implemented')

  def get(self):
      raise NotImplemented('get', 'This action should be implemented')

  def get_list(self):
      raise NotImplemented('get_list', 'This action is not implemented')

  def _execute(self, request):
      try:
	#print dir(request)
	#print request.data
	#print request.headers
	#print request.get_method()
	#print request.get_full_url()
        self.response = urllib2.urlopen(request)
      except urllib2.HTTPError, e:
	#print self.response.info()
        print >> sys.stderr,"error"
        print >> sys.stderr,e
        print >> sys.stderr,e.read()
        return

      #print >> sys.stderr,"----------- response ----------"
      #print >> sys.stderr,self.response.code, self.response.msg
      #print >> sys.stderr,"----------- headers ----------"
      #print >> sys.stderr,self.response.headers
      #print >> sys.stderr,"-------- body --------"
      #print self.response.read()

