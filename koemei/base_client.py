import sys
import urllib2
import traceback
from koemei.utils import log, settings
from copy import copy
import urllib

class BaseClient(object):
    """
    This is the base client, implements basic rest methods
    """

    def __init__(self):
        """
        Create the api client
        """

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

    def path(self, args, url_params=None):
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

            # add request parameters
            if url_params is not None:
                path = path + '?'
                for key, value in url_params.iteritems():
                    path = path + '&' + key + '=' + urllib.quote(str(value), safe='')

            return path
        except Exception, e:
            log.error("Error building path with params:")
            log.error(args)
            log.error(e)
            log.error(traceback.format_exc())
            raise

    def request(self, url, data=None, headers={}, url_params=None, accept=None):
        """
        GET call at the given url
        @params url: the path to the method to call, relative to the api root url
        @params params: dictionary containing the parameters for the rest call
        @return rest response in json
        """
        self._reset_headers(headers, accept)
        log.debug("Making request to %s" % self.path(url, url_params))
        log.debug(url)
        log.debug(data)
        log.debug(headers)

        request = urllib2.Request(self.path(url, url_params), data=data, headers=headers)

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

    def _reset_headers(self, headers={}, accept=None):
        self.headers = headers
        import base64

        if accept is None:
            accept = settings.get('base', settings.get('base', 'accept.default'))
        else:
            accept = settings.get('base', 'accept.%s' % accept)

        if self.username != "" and self.password != "":
            auth_string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
            self.headers.update({'authorization': 'basic %s' % auth_string,
                                 'accept': accept, })
        else:
            log.error('The username and/or password are empty.')
            exit()