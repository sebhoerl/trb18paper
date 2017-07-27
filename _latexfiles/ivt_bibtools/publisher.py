#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import string
import operator

from .strings import toIdentifier

from .entity import Entity

from .six import u

class Publisher(Entity):
    _publisherRegex= re.compile("^[ \t]*([^=]*[^ \t=])[ \t]*=[ \t]*([^ \t]+)[ \t]*$")

    def __init__(self, name, options):
        super(Publisher, self).__init__(options)
        self._keyValue = name


    def getKeyGenerator(self):
        key = self._key
        while True:
            yield key
            key = key + "Q"


    def checkAndFixValue(self):
        keyValueMatch = self._publisherRegex.match(self._keyValue)
        if keyValueMatch is None:
            raise Exception(u("Invalid publisher format: %s. Specify publisher as PublisherName=Key.") % self._keyValue)

        self._publisher = keyValueMatch.group(1)
        self._key = keyValueMatch.group(2)
        

    def getValue(self):
        return self._publisher


    def getValues(self):
        return [self._publisher]


    def getSeparator(self):
        return "Publishers"


    def getKeyPartWidth(self):
        return 25


if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        class TestOptions:
            pass
        
        def test_getKeyGenerator(self):
            j = Publisher("Publisher=J", self.TestOptions)
            j.checkAndFixValue()
            gen = j.getKeyGenerator()
            
            self.assertEqual(next(gen), "J", self.TestOptions)
            self.assertEqual(next(gen), "JQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQQ", self.TestOptions)
            self.assertEqual(next(gen), "JQQQQ", self.TestOptions)

        def test_checkValue(self):
            a1 = Publisher(u" \t Publisher \t = \t P \t ", self.TestOptions)
            a1.checkAndFixValue()
            self.assertEqual(a1.getValue(), u"Publisher")
            
            a2 = Publisher(u"Publisher", self.TestOptions)
            self.assertRaises(Exception, a2.checkAndFixValue)

        def test_getValues(self):
            j = Publisher(u" \t Publisher \t = \t P \t ", self.TestOptions)
            j.checkAndFixValue()
            self.assertTrue(hasattr(j.getValues(), "__iter__"))
            self.assertEqual(len(j.getValues()), 1)

    unittest.main()
