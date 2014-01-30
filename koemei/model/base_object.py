import sys
import urllib2
from exceptions import NotImplementedError
from koemei.utils import settings, log


class BaseObject(object):

    def __init__(self, fields=None):
        if fields is not None:
            for field_name in fields:
                setattr(self, field_name, fields[field_name])

    @classmethod
    def get(cls, deleted=False, *args, **kwargs):
        raise NotImplementedError('get', 'This action should be implemented')

