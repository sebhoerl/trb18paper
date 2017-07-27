#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import os.path
import re
import codecs
import sys

from .strings import keyValueEntryRegex

def safeRename(src, dest):
    if sys.platform == "win32":
        os.unlink(dest)
    os.rename(src, dest)

def getTempFileName(fileName):
    (dir, name) = os.path.split(fileName)
    return os.path.join(dir, ".%s" % name)

if __name__=='__main__':
    import unittest
    class TestSafeRename(unittest.TestCase):
        _f1 = "f1"
        _f2 = "f2"
        
        def setUp(self):
            with open(self._f1, "w"):
                pass
            with open(self._f2, "w"):
                pass
            
        def test_safeRename(self):
            safeRename(self._f1, self._f2)

        def tearDown(self):
            try:
                os.unlink(self._f1)
            except:
                pass
            
            try:
                os.unlink(self._f2)
            except:
                pass

    class TestGetTempFileName(unittest.TestCase):
        def test_getTempFileName(self):
            self.assertEqual(getTempFileName("f1"), ".f1")
            self.assertEqual(getTempFileName("a/f1"), os.path.normpath("a/.f1"))

    unittest.main()
    