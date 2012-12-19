#!/usr/bin/python
# ==============================================================
#  (c) 2010 Koemei SA
#  Author: John Dines.

# =======================================================
# IMPORTS
# =======================================================

import urllib2, sys, os, urllib

# for streaming
from encode import multipart_encode, MultipartParam
from streaminghttp import register_openers

# =======================================================
# METHODS
# =======================================================

def create_metadata(metadataFilename):
  fp = open(metadataFilename,"r")
  metadata = fp.read()
  fp.close()

  return metadata

import hashlib
def md5_for_file(filename, block_size=2**20):
    f=open(filename, 'r')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()

import re

def make_request(method,accept,path,audioFilename, metadataFilename):
  datagen = {}
  headers = {}

  dest = 'http://www.koemei.com/REST/'
  #dest = 'http://www.koemei.com/REST/'
  #dest = 'http://localhost:8080/REST/'

  print >> sys.stderr, 'making %s request to: %s%s' % (method,dest,path)

  import base64
  auth_string = base64.encodestring('%s:%s' % ('myemail address', 'changeme'))[:-1]
  headers.update( { 'authorization': 'basic %s' % auth_string,
                    'accept' : accept,})

  if method == 'GET':

    return urllib2.Request(dest+path, headers=headers)

  if method == 'HEAD':

    request = urllib2.Request(dest+path, headers=headers)
    request.get_method = lambda : 'HEAD'

    return request 

  if method == 'DELETE':

    request = urllib2.Request(dest+path, headers=headers)
    request.get_method = lambda: 'DELETE'

    return request

  if method == 'POST':
      if path == 'media' :
          datagen = {}

          if len(audioFilename) > 0:
            if 'http' in audioFilename :
                path = path +"?media="+ urllib.quote(audioFilename)
                datagen = "" # should not be empty dict but empty string!
            else :
                if len(metadataFilename) > 0:
                    datagen, headers_ = multipart_encode({ 'metadata' : create_metadata(metadataFilename),
                                                         'media' : open(audioFilename, "rb") })
                else:
                    datagen, headers_ = multipart_encode({ 'media' : open(audioFilename, "rb") })
                headers.update(headers_)


          print >> sys.stderr, "request headers: ", headers

          request = urllib2.Request(dest+path, data= datagen, headers=headers)

          return request
      elif path == 'kobjects' :
          datagen = {}
          request = urllib2.Request(dest+path, data="", headers=headers)
          return request
      elif 'transcribe' in path :
          # transcription request
          datagen = {}
          request = urllib2.Request(dest+path, data="", headers=headers)
          return request
      elif 'kobjects' in path and 'media' in path :
          # upload a media to an existing kobject
          datagen = {}

          if len(audioFilename) > 0:
              if len(metadataFilename) > 0:
                  datagen, headers_ = multipart_encode({ 'metadata' : create_metadata(metadataFilename),
                                                         'media' : open(audioFilename, "rb") })
              else:
                  datagen, headers_ = multipart_encode({ 'media' : open(audioFilename, "rb") })
              headers.update(headers_)


          print >> sys.stderr, "request headers: ", headers

          request = urllib2.Request(dest+path, data= datagen, headers=headers)

          return request

# =======================================================
# MAIN
# =======================================================

def main():
  if len(sys.argv) <= 1:
    print >> sys.stderr, "Usage: API.py <method> <accept> <path> [upload] [metadata]"
    exit()

  # user input
  method = sys.argv[1]
  accept = sys.argv[2]
  path = sys.argv[3]
  if len(sys.argv) > 4 :
    if 'http' not in sys.argv[4] :
        audioFilename = os.path.abspath(sys.argv[4])   # optional
    else :
        audioFilename = sys.argv[4]
  else:
    audioFilename = ''
  if len(sys.argv) > 5:
    metadataFilename = sys.argv[5]   # optional
  else:
    metadataFilename = ''
  
  register_openers()

  request = make_request(method,accept, path, audioFilename, metadataFilename)

  # Actually do the request, and get the response
  try:
    response = urllib2.urlopen(request)
  except urllib2.HTTPError, e:
    print >> sys.stderr,"error"
    print >> sys.stderr,e
    print >> sys.stderr,e.read()
    return
    
  print >> sys.stderr,"----------- response ----------"
  print >> sys.stderr,response.code, response.msg
  print >> sys.stderr,"----------- headers ----------"
  print >> sys.stderr,response.headers
  print >> sys.stderr,"-------- body --------"
  print response.read()

if __name__=="__main__":
  main()
