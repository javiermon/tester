#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
"""Settings loader
"""

import ConfigParser
import logging

log = logging.getLogger('tester')
INI = 'settings.ini'

class Settings(object):
    """Application Settings
    """
    __shared_state = {'cp': ConfigParser.RawConfigParser(allow_no_value=True),}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.file = INI
        self.cp.read(self.file)
        
    def getStringOption(self, section, option):
        """Get a string option from a section
        """
        return self.cp.get(section, option)

    def getBooleanOption(self, section, option):
        """Get a boolean option from a section
        """
        return self.cp.getboolean(section, option)

    def getIntOption(self, section, option):
        """Get an integer option from a section
        """
        return self.cp.getint(section, option)

    def getSection(self, section):
        """Returns the whole section in a dictionary
        """
        options = self.cp.options(section)
        result = {}
        for option in options:
            result[option] = self.cp.get(section, option)
        return result

    def getListSection(self, section):
        """Returns a list of items
        useful for lists of items without values
        """
        return self.cp.options(section)
