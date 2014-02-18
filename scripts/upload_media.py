from mainAPI import *

import json, csv

# =======================================================
# USAGE
# =======================================================

def usage():
        print """
Synopsis:
    Uses Python API client to do some batch processing, in this 
    case bulk media transcribe. 

Usage:
    python upload_media.py [options] <file_list>

Arguments:
    <file_list>               List of file paths / URLs to be uploaded
                              (list may be CSV of URL,service,item_id)

Options:
    -b, --begin               Start downloading from line number
    -c, --count               Limit number of media to transcribe in this request
    -s, --service             Service from which the upload is being made
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
    begin = 0
    service = None

    opts, args = getopt.getopt(argv[1:], "vhc:s:b:", ["verbose", "help", "count=", "begin=", "service="])

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-v","--verbose"):
            # TODO: the goggles do nothing!
            verbose = True
        elif o in ("-c", "--count"):
            count = int(a)
        elif o in ("-b", "--begin"):
            begin = int(a)
        elif o in ("-s", "--service"):
            service = str(a)
        else:
            print 'Wrong option '+o+'\n'
            usage()

    if len(args) != 1:
        print 'You need to provide a file list!'
        usage()

    filelistFile = args[0]
    filelist = []
    with open(filelistFile) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            filelist.append(tuple(row))

    # first get list of uploads
    register_openers()

    uid = None
    process_id = None
    accept = 'text/xml'
    metadataFilename = None
    transcriptFilename = None
    username='changeme'
    password='changeme'

    object_type = 'Media'
    action = 'create'

    for f in filelist[begin:begin+count] if count else filelist[begin:]:
        print "Uploading: %s" % f[0]

        audioFilename = f[0]
        try:
            item_id = f[1]
        except IndexError:
            item_id = None
            service = None

        media = new Media
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
