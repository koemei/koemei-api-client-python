import sys
import urllib2
import traceback
from koemei.utils import log, settings
from copy import copy


class BaseClient(object):
    """
    This is the base client, implements basic rest methods
    """

    def __init__(self):
        """
        Create the api client
        """

        self.accept = settings.get('base', 'accept')

        # init config
        try:
            self.username = settings.get("credentials", "username")
            self.password = settings.get("credentials", "password")
        except Exception,e:
            log.error("Error getting api credentials from settings file")
            log.error(e)
            log.error(traceback.format_exc())
            raise e
        self._reset_headers()

        try:
            self.base_path = settings.get("base", "paths.api")
        except Exception,e:
            log.error("Error getting api path from settings file")
            log.error(e)
            log.error(traceback.format_exc())
            raise e

        self.response = None

    def path(self, args):
        """
        Build path for api call
        @params url path params
        """
        try:
            path_array = copy(args)
            path_array.reverse()
            path_array.append(self.base_path)
            path_array.reverse()
            path = '/'.join(path_array)
            return path
        except Exception, e:
            log.error("Error building path with params:")
            log.error(args)
            log.error(e)
            log.error(traceback.format_exc())
            raise

    def request(self, url, data=None, headers={}):
        """
        GET call at the given url
        @params url: the path to the method to call, relative to the api root url
        @params params: dictionary containing the parameters for the rest call
        @return rest response in json
        """
        self._reset_headers(headers)
        log.debug("Making request to %s" % self.path(url))
        log.debug(url)
        log.debug(data)
        log.debug(headers)

        request = urllib2.Request(self.path(url), data=data, headers=headers)

        try:
            #print dir(request)
            #print request.data
            #print request.headers
            #print request.get_method()
            #print request.get_full_url()
            return urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            #print self.response.info()
            print >> sys.stderr, "error"
            print >> sys.stderr, e
            print >> sys.stderr, e.read()
            return

            #print >> sys.stderr,"----------- response ----------"
            #print >> sys.stderr,self.response.code, self.response.msg
            #print >> sys.stderr,"----------- headers ----------"
            #print >> sys.stderr,self.response.headers
            #print >> sys.stderr,"-------- body --------"
            #print self.response.read()

    def _reset_headers(self, headers={}):
        self.headers = headers
        import base64

        if self.username != "" and self.password != "":
            auth_string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
            self.headers.update({'authorization': 'basic %s' % auth_string,
                                 'accept': self.accept, })

        else:
            print >> sys.stderr, 'The username and/or password are empty.'
            exit()