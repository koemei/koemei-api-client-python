#!/usr/bin/python
# ==============================================================
#  (c) 2010 Koemei SA
#  Author: Marina Zimmermann, John Dines.

# =======================================================
# IMPORTS
# =======================================================

import urllib2, sys, os, urllib
import getopt

# for streaming
from streaminghttp import register_openers


# =======================================================
# USAGE
# =======================================================

def usage():
        print """
Synopsis:
    Python API client to be used from the command line

Usage:
    python mainAPI.py [options] <object_type> <action> [<accept>]

Arguments:
    <object_type>             The object type to be used:
                              KObject, Media, Transcript or Process
    <action>                  The action to be taken:
                              KObject: get (requires uid), delete (requires uid), get_list, create
                              Media: get (requires uid), get_list, create, transcribe (requires uid)
                              Transcript: get (requires uid)
                              Process: get (requires uid and process_id)
    <accept>                  Accept type: default text/xml

Options
    -i, --uid                 ID for the KObject/Media/Transcript item
    -p, --process_id          Process ID for transcription process
    -u, --upload              Path or link to an audiofile to be uploaded
    -m, --metadata            Metadata for the audiofile
    -v, --verbose             Print out details about the process, handy for debugging
    -h, --help                Print this message ;-)

Example
    python mainAPI.py -v -i {uid} Media get

""";
        sys.exit()

# =======================================================
# OBJECTS
# =======================================================

from KObject import KObject
from Media import Media
from Process import Process
from Transcript import Transcript

# =======================================================
# MAIN
# =======================================================

def main(argv=None):

    if argv is None:
        argv = sys.argv

    verbose = False
    uid = ""
    process_id = ""
    audioFilename = ""
    metadataFilename = ""
    accept = 'text/xml'

    # NEED TO SPECIFIY USERNAME AND PASSWORD HERE
    username = ''
    password =  ''

    opts, args = getopt.getopt(argv[1:], "vhi:p:u:m:", ["verbose" ,"help", "uid=", "process_id=", "upload=", "metadata="])

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-v","--verbose"):
            verbose = True
        elif o in ("-i", "--uid"):
            uid = str(a)
        elif o in ("-p", "--process_id"):
            process_id = str(a)
        elif o in ("-u", "--upload"):
            audioFilename = str(a)
        elif o in ("-m", "--metadeta"):
            metadataFilename = str(a)
        else:
            print 'Wrong option '+o+'\n'
            usage()

    if (len(args) < 2):
        print 'You need to provide an object type and action!'
        usage()

    object_type = args[0]
    action = args[1]

    if (len(args) == 3):
        accept = args[2]

    register_openers()

    # Create an instance of the <object_type> given as input argument with the provided arguments
    inst = globals()[object_type](accept, username, password, uid, process_id, audioFilename, metadataFilename)

    # Call the <action> indicated in the input arguments
    func = getattr(inst, action)
    func()

    print >> sys.stderr,"----------- response ----------"
    print >> sys.stderr,inst.response.code, inst.response.msg
    print >> sys.stderr,"----------- headers ----------"
    print >> sys.stderr,inst.response.headers
    print >> sys.stderr,"-------- body --------"
    print inst.response.read()

if __name__=="__main__":
  main()

