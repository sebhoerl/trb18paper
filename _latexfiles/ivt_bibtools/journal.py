#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import string
import operator

from .strings import toIdentifier

from .entity import Entity

from .six import u

class Journal(Entity):
    _journalRegex= re.compile("^[ \t]*([^=]*[^ \t=])[ \t]*=[ \t]*([^ \t]+)[ \t]*$")

    def __init__(self, name, options):
        super(Journal, self).__init__(options)
        self._keyValue = name


    def getKeyGenerator(self):
        key = self._key
        while True:
            yield key
            key = key + "Q"


    def checkAndFixValue(self):
        keyValueMatch = self._journalRegex.match(self._keyValue)
        if keyValueMatch is None:
            raise Exception(u("Invalid journal format: %s. Specify journal as JournalName=Key.") % self._keyValue)

        self._journal = keyValueMatch.group(1)
        self._key = keyValueMatch.group(2)
        

    def getValue(self):
        return self._journal


    def getValues(self):
        return [self._journal]


    def getSeparator(self):
        return "Journals and Magazines"


    def getKeyPartWidth(self):
        return 25


if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        class TestOptions:
            pass
        
        def test_getKeyGenerator(self):
            j = Journal("Journal=J", self.TestOptions)
            j.checkAndFixValue()
            gen = j.getKeyGenerator()
            
            self.assertEqual(next(gen), "J", self.TestOptions)
            self.assertEqual(next(gen), "JQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQQQ", self.TestOptions)

        def test_checkValue(self):
            a1 = Journal(u" \t Journal \t = \t J \t ", self.TestOptions)
            a1.checkAndFixValue()
            self.assertEqual(a1.getValue(), u"Journal")
            
            a2 = Journal(u"Journal", self.TestOptions)
            self.assertRaises(Exception, a2.checkAndFixValue)

        def test_getValues(self):
            j = Journal(u" \t Journal \t = \t J \t ", self.TestOptions)
            j.checkAndFixValue()
            self.assertTrue(hasattr(j.getValues(), "__iter__"))
            self.assertEqual(len(j.getValues()), 1)

    unittest.main()
