#!/usr/bin/python
# ==============================================================
#  (c) 2010 Koemei SA
#  Author: Marina Zimmermann.

# ==============================================================
# EXAMPLE USAGE:
# 1) Upload a media file
# 2) Request a transcript
# 3) Check progress of transcription  repeatedly
#    (might take very long and is not necessarily recommended)
# 4) Save transcript
#    (can also be done separately using the Transcript object)
# ==============================================================

import sys, re, time

# for streaming
from streaminghttp import register_openers

def main():

    username = ""
    password = ""

    from Media import Media

    register_openers()

    # 1) Upload a media file
    inst = Media(accept="text/xml", username=username, password=password, audioFilename="test.mp3")

    inst.create()

    # extract the uid given to this media item
    if inst.response.code == 200:
       print "Media item has been created successfully"
       search = None
       search = re.search("<id>(.*)</id>", inst.response.read())
       if search != None:
          uid = search.group(1)
          uid = str(uid)
          print "The following uid has been extracted: %s" % uid
       else:
          print >> sys.stderr, "An error occured trying to extract the uid"

    else:
       print >> sys.stderr, "-------- An error occurred, response: --------"
       print >> sys.stderr, inst.response.code, inst.response.msg
       print >> sys.stderr, "-------- Headers --------"
       print >> sys.stderr, inst.response.headers

    inst.uid = uid

    # 2) Request a transcript of the just uploaded media item
    inst.transcribe()

    # extract the process id given to this process:
    if inst.response.code == 202:
       print "Transcription has been accepted"
       search = None
       search = re.search('<atom:link href="https://www.koemei.com/REST/media/.*/transcribe/(.*)" rel="self"></atom:link>', inst.response.read())
       if search != None:
          process_id = search.group(1)
          print "The following process id has been extracted: %s" % process_id
       else:
          print >> sys.stderr, "An error occured trying to extract the process id"

    else:
       print >> sys.stderr, "-------- An error occurred, response: --------"
       print >> sys.stderr, inst.response.code, inst.response.msg
       print >> sys.stderr, "-------- Headers --------"
       print >> sys.stderr, inst.response.headers

    time.sleep(5)

    from Process import Process

    inst = Process(accept="text/xml", username=username, password=password, uid=uid, process_id=process_id)

    transcript_ready = False

    while (transcript_ready == False):

         inst.get()

         # extract the progress of this process and if completed the transcript id:
         if inst.response.code == 200:
            transcript = open('transcript.xml', 'w+')
            transcript.write(inst.response.read())
            transcript.close()

            transcript = open('transcript.xml', 'r')
            for e in transcript.readlines():
                e = e.strip()
                search = None
                search = re.search('<progress>(.*)</progress>', e)
                if search != None:
                   print "Transcription still in progress"
                   progress = search.group(1)
                   print "The process is at %s %%" % progress
                   break
            transcript.close()
            # if no progress info has been found, check if the transcript is ready:
            if search == None:
               transcript = open('transcript.xml', 'r')
               for e in transcript.readlines():
                   e = e.strip()
                   search = None
                   search = re.search('<segmentation>', e)
                   if search != None:
                      transcript_ready = True
                      print "Transcription has finished, the transcript has been saved to transcript.xml"
                      break
            transcript.close()
            if search == None:
               print >> sys.stderr, "An error occured trying to extract the progress"

         else:
            print >> sys.stderr, "-------- An error occurred, response: --------"
            print >> sys.stderr, inst.response.code, inst.response.msg
            print >> sys.stderr, "-------- Headers --------"
            print >> sys.stderr, inst.response.headers

         if transcript_ready == False:
            time.sleep(600)


if __name__ == "__main__":
   main()
