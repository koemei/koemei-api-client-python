# -*- coding: utf-8 -*-

import os
import traceback

from ConfigParser import SafeConfigParser
from ConfigParser import Error as ConfigParserError

from koemei.exceptions import SettingsFileNotFoundError


def read_settings_file():
    """
    Read the settings.ini file located at the root of this project
    """
    # read settings
    settings_file_path = "settings.ini"
    settings = None
    try:
        if os.path.exists(settings_file_path):
            settings = SafeConfigParser()
            settings.read(settings_file_path)
        else:
            raise SettingsFileNotFoundError("Settings file not found, please copy settings.example.ini to settings.ini and fill in your details")
    except ConfigParserError, e:
        print "Error parsing settings file: "
        print e
        print traceback.format_exc()
        raise e
    return settings


def read_file(filename):
    fp = open(os.path.abspath(filename), "r")
    file_content = fp.read()
    fp.close()

    return file_content

settings = read_settings_file()

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(settings.get('logging', 'level'))

def check_file_extension(file_path, authorized_file_types):
    try:
        fileName, fileExtension = os.path.splitext(file_path)
        if fileExtension.split('.')[1] in authorized_file_types:
            return True
        return False
    except Exception, e:
        return False
