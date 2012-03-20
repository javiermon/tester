#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
"""Testing framework

This module will search for scripts in the same directory named
XYZtest.py.  Each such script should be a test suite that tests a
module through PyUnit.

Example Usage:
sudo ./tester.py --file=regression.tests --verbosity=5 --settings=settings.ini

Parameters:
-h, --help: Print this help
--file=file: The regression test suite
--verbosity=X: The verbosity for pyunit
--settings=file: Use this settings file

"""

import sys, os, re, unittest
import getopt
import logging
import log
import settings
import time

logger = logging.getLogger('tester')
COMMENT = '#'
FAILURES='failures.tests'
MARKER = "**********************************************************************"


class TESTER(object):
    def __init__(self, suite, verbosity, stderr=sys.stderr, stdout=sys.stdout):
        self.verbosity = verbosity
        self.stderr = stderr
        self.stdout = stdout
        self.failures = None
        self.suite = suite
        self.stream = log.TestLogger(self.stderr, suite.countTestCases())

    def runTest(self):
        sys.stderr = self.stderr
        sys.stdout = self.stdout
                
        logger.debug("Running regression tests")
        results = unittest.TextTestRunner(verbosity=self.verbosity, stream=self.stream).run(self.suite)
        self.failures = results.failures + results.errors
        return self.failures == []
        
    def generateFailures(self):
        """Creates a file with the failures
        """
        if self.failures in ([], None):
            return False
        failedTests = open(FAILURES, 'w')
        # TODO: append timestamp
        failedTests.write("# Failed tests file:\n")
        failedTests.write("# The following tests failed:\n")

        results = []
        for (failure, traceback) in self.failures:
            # for now, we record the full test that failed.
            fullname = failure.id()
            testname = fullname.split('.')[0]
            if testname not in results:
                results.append(testname)
                failedTests.write("%s.py\n" % testname)

        failedTests.close()
        return True

    def loadSuiteDescriptions(self):
        descriptions = []
        try: # FIXME: I don't know why there's so much nesting?
            for ssuite in self.suite:
                for sssuite in ssuite:
                    for test in sssuite:
                        descriptions.append(test.shortDescription())

        except Exception, e:
            logger.debug("Could not load description from test %s" % e)
        return descriptions


def regressionTest(filetest, inifile=None):
    """Regression Tests launcher
    """
    if inifile is not None:
        settings.INI = inifile
    try:
        regression_file = file(filetest)
    except IOError:
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        regression_file = file("%s/%s" % (path, filetest))
    logger.debug("Regression test file: %s" % filetest)    
    logger.debug("Settings file: %s" % settings.INI)    

    stripendline = lambda s: s.replace('\n','')
    files = [stripendline(line) for line in regression_file if not line.startswith(COMMENT)]
    return createRegressionTest(files)

def createRegressionTest(files):
    if files == []:
        return None

    test = re.compile("test\.py$", re.IGNORECASE)          
    files = [f for f in files if test.search(f)]

    logger.debug("Collected %d tests:" % len(files))
    for f in files:
        logger.debug("\t%s" % f)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = [filenameToModuleName(f) for f in files]
    modules = [ __import__(m) for m in moduleNames ]
    load = unittest.defaultTestLoader.loadTestsFromModule  
    return unittest.TestSuite([ load(m) for m in modules ])


def main():
    """main. Parses options and launches ats accordingly
    """
    log.configureLogger(log=log.testlog, fileLog=log.TESTLOGFILE, format=log.TESTFORMAT, truncate=True)
    log.configureLogger(log=log.log, fileLog=log.LOGFILE)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "file=", "verbosity=",
                                                       "settings="])    
        # process options
        testfile = None
        inifile = None

        verbosity = 2        
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                sys.exit(0)
            if o in ("--file",):
                testfile = a
                logger.debug("starting %s" % testfile)
            if o in ("--settings",):
                inifile = a
            if o in ("--verbosity",):
                verbosity = a

        if testfile is None:
            sys.stderr.write("Error, missing testfile")
            print __doc__
            sys.exit(2)

        suite = regressionTest(testfile, inifile)
        tester = TESTER(suite, verbosity)
        # TODO: runTest gives a return value
        tester.runTest()
        tester.generateFailures()

        sys.exit(0)
	
    except getopt.error, msg:
        sys.stderr.write("%s" % msg)
        sys.stderr.write("for help use --help")
        sys.exit(2)

if __name__ == "__main__":
    main()
