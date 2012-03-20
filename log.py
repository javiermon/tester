#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-

import logging
import time, datetime

log = logging.getLogger('tester')
testlog = logging.getLogger('tester-test') 

LOGFILE = 'tester.log' 
TESTLOGFILE = 'tester-test.log' 
TESTFORMAT = "%(message)s"
FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"

class TestLogger(object):
    """Useful to log to logfile the running tests
    """
    def __init__(self, out, ntest):
        self.file = out
        t = datetime.datetime.now()
        epoch = time.mktime(t.timetuple())
        timestampt = datetime.datetime.fromtimestamp(epoch).ctime()

        self.write("%s\nstarting %d tests\n" % (timestampt, ntest))

    def __getattr__(self, atr):
        return getattr(self.file, atr)
    
    def write(self, s):
        self.file.write(s)
        testlog.debug(s)        
        #log.info(s)        


def configureLogger(log, fileLog, format = FULLFORMAT, truncate=False):
    if truncate:
        open(fileLog, 'w').close()
    # file logging:
    logfile = logging.FileHandler(fileLog)
    formatter = logging.Formatter(format)
    logfile.setFormatter(formatter)
    # DOESNT WORK!
    logfile.setLevel(logging.DEBUG)

#    # add all handlers:
    log.addHandler(logfile)
#    # stdout logging:
#    console = logging.StreamHandler()
#    #console.setLevel(logging.DEBUG)
#    console.setFormatter(formatter)
#    log.addHandler(console)
#    # global debug level:
    log.setLevel(logging.DEBUG)

