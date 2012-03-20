#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
"""Unit test sample
"""
import unittest

class TestingTest(unittest.TestCase):

    def setUp(self):
        """Set's up the test"""
        pass

    def testTest(self):
        """Checks true"""
        # The fonera is on:
        self.assertTrue(1 == 1)
            
        
if __name__ == '__main__':
    unittest.main()
