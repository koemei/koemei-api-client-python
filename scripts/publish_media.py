
from mainAPI import *

import json

# =======================================================
# USAGE
# =======================================================

def usage():
        print """
Synopsis:
    Uses Python API client to do some batch processing, in this 
    case bulk media transcribe. 

Usage:
    python transcribe_media.py [options]

Options
    -s, --service             Publish to this service (if you can!)
    -c, --count               Limit number of media to transcribe in this request
    -v, --verbose             Print out details about the process, handy for debugging
    -h, --help                Print this message ;-)

""";
        sys.exit()

# =======================================================
# MAIN
# =======================================================


def main(argv=None):

    if argv is None:
        argv = sys.argv

    verbose = False
    count = None
    service = None

    opts, args = getopt.getopt(argv[1:], "vhc:s:", ["verbose", "help", "count=", "service="])

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-v","--verbose"):
            # TODO: the goggles do nothing!
            verbose = True
        elif o in ("-c", "--count"):
            count = int(a)
        elif o in ("-s", "--service"):
            service = str(a)
        else:
            print 'Wrong option '+o+'\n'
            usage()

    # first get list of uploads
    register_openers()

    uid = None
    process_id = None
    accept='application/json'
    audioFilename = None
    metadataFilename = None
    transcriptFilename = None
    item_id = None
    username='changeme'
    password='changeme'

    object_type = 'Media'
    action = 'get_list'
    #status = [1]
    status = [ STATUS_CODE['ASR'] ]

    inst = globals()[object_type](accept, username, password, uid, process_id,
                                  audioFilename, metadataFilename, transcriptFilename,
                                  service, item_id, count, status)
    try:
        func = getattr(inst, action)
        func()
    except urllib2.HTTPError, e:
        print >> sys.stderr, "error"
        print >> sys.stderr, e
        print >> sys.stderr, e.read()
        raise e

    media_list = json.loads(inst.response.read())

    for m in media_list['media'][:count]:
    #if True:
        if m['progress'] == 100:
        #if True:
            print m['clientfilename'], m['status']

            accept = 'application/json'
            audioFilename=None
            metadataFilename=None
            uid = m['uuid']

            action = 'publish'
            inst = globals()[object_type](accept, username, password, uid, process_id, audioFilename, metadataFilename, transcriptFilename, service, item_id)
            try:
                func = getattr(inst, action)
                func()
            except urllib2.HTTPError, e:
                print >> sys.stderr,"error"
                print >> sys.stderr,e
                print >> sys.stderr,e.read()


if __name__=="__main__":
    main()

