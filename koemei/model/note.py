import urllib
from koemei.utils.encode import multipart_encode, MultipartParam
from koemei.utils import log, settings, read_file, check_file_extension
from koemei.utils.streaminghttp import register_openers
import json

from base_object import BaseObject


class Note(BaseObject):

    def __init__(self, fields={}):
        """
        @param fields [Hash]
        """
        super(Note, self).__init__(fields=fields)

    @classmethod
    def get(cls, client, uuid, deleted=False):
        url = [settings.get('base', 'paths.api.notes'), uuid]
        response = client.request(url=url)
        response_json = json.loads(response)
        return Note(fields=response_json["note"])

    @classmethod
    def get_all(cls, client, *args, **kwargs):
        url_data = {}
        if kwargs.get('status'):
            url_data.update({'status_filter':  '-'.join(map(lambda x: str(x), kwargs.get('status')))})
        if kwargs.get('search_query'):
            url_data.update({'search_query': kwargs.get('search_query')})

        url_data = urllib.urlencode(url_data)
        url = [settings.get('base', 'paths.api.notes'), url_data]
        response = client.request(url=url)
        response_json = json.loads(response)

        media = []

        for media_item in response_json['notes']:
            media.append(Note(fields=media_item))
        return media

    @classmethod
    def create(
        cls,
        client,
        media_item,
        parent_note=None,
        **kwargs):
        """
        Create a note.
        """

        data = {}
        # TODO : fill in note params
        headers = {}
        url = [settings.get('base', 'paths.api.notes')]

        register_openers()
        response = client.request(url=url, data=data, headers=headers)
        response_json = json.loads(response)
        note = Note(fields=response_json['note'])

        return note


"""

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
"""