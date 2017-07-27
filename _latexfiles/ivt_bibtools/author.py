#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import string
import operator
import functools

from .strings import toIdentifier

from .entity import Entity

from .six import u

class Author(Entity):
    _authorRegex = re.compile("^([^,]*)(?:|, +(.*))$")
    _strongAuthorRegex = re.compile("^([^,]*), +(.*)$")
    _firstLastAuthorRegex = re.compile("^(.*) +([^ ]+)$")
    _spacesRegex = re.compile(" +")

    def __init__(self, name, options):
        super(Author, self).__init__(options)
        self._author = name


    def getKeyGenerator(self):
        yield self._getKey(0)
        key = self._getKey(1)
        while True:
            yield key
            key = key + "Q"


    def checkAndFixValue(self):
        if self._strongAuthorRegex.match(self._author) is None:
            if not self._options.firstLastName:
                raise Exception(u("Invalid author format: %s. Specify author as LastName, FirstName(s). Or leave out the -n switch.") % self._author)

            firstLastMatch = self._firstLastAuthorRegex.match(self._author)
            if firstLastMatch is None:
                raise Exception(u("Invalid author format: %s. Specify author as LastName, FirstName(s) or FirstName(s) LastName.") % self._author)

            self._author = firstLastMatch.group(2) + u(", ") + firstLastMatch.group(1)
            assert self._strongAuthorRegex.match(self._author)            
        

    def getValue(self):
        return self._author


    def getValues(self):
        shortenedAuthor = self._shortenAuthor()
        if shortenedAuthor == self._author:
            return [self._author]
        
        return [self._author, shortenedAuthor]


    def getSeparator(self):
        return "author names"


    def _getKey(self, index):
        (lastName, firstName) = self._authorRegex.match(self._author.strip()).group(1, 2)
        if index == 0:
            return toIdentifier(lastName)
        else:
            firstNameKey = functools.reduce(operator.concat, [s[0] for s in self._spacesRegex.split(firstName)]).upper()
            return toIdentifier(lastName + firstNameKey)


    def _shortenAuthor(self):
        (lastName, firstName) = self._authorRegex.match(self._author.strip()).group(1, 2)
        firstNames = ""
        if not (firstName is None):
            firstNames = ", " + u(" ").join([s[0] + u(".") for s in self._spacesRegex.split(firstName)]).upper()
        return lastName + firstNames


if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        class TestOptions:
            pass
        
        def test_getKey(self):
            self.assertEqual(Author(u"Müller, Kirill", self.TestOptions)._getKey(0), "Mueller")
            self.assertEqual(Author("Axhausen, Kay Werner", self.TestOptions)._getKey(1), "AxhausenKW")
            self.assertEqual(Author("O'Hara, R.", self.TestOptions)._getKey(0), "OHara")
            self.assertEqual(Author("O'Leary, Bernard", self.TestOptions)._getKey(1), "OLearyB")

        def test_getKeyGenerator(self):
            gen = Author("Axhausen, Kay Werner", self.TestOptions).getKeyGenerator()
            self.assertEqual(next(gen), "Axhausen", self.TestOptions)
            self.assertEqual(next(gen), "AxhausenKW", self.TestOptions)
            self.assertEqual(next(gen), "AxhausenKWQ", self.TestOptions)
            self.assertEqual(next(gen), "AxhausenKWQQ", self.TestOptions)
            self.assertEqual(next(gen), "AxhausenKWQQQ", self.TestOptions)

        def test_checkValue(self):
            class optionsEmpty:
                firstLastName = False
            
            class optionsWithFirstLastMatch:
                firstLastName = True

            a1 = Author(u"Müller, Kirill", optionsEmpty)
            a1.checkAndFixValue()
            self.assertEqual(a1.getValue(), u"Müller, Kirill")
            
            a2 = Author(u"Christof Zöllig", optionsEmpty)
            self.assertRaises(Exception, a2.checkAndFixValue)
            
            a3 = Author(u"Patrick Schirmer", optionsWithFirstLastMatch)
            a3.checkAndFixValue()
            self.assertEqual(a3.getValue(), u"Schirmer, Patrick")

        def test_shortenAuthor(self):
            self.assertEqual(Author("Bodenmann, Balz R.", self.TestOptions)._shortenAuthor(), "Bodenmann, B. R.")
            
        def test_getValues(self):
            self.assertTrue(hasattr(Author("Horni, A.", self.TestOptions).getValues(), "__iter__"))
            self.assertEqual(len(Author("Horni, A.", self.TestOptions).getValues()), 1)
            self.assertEqual(set(Author("Meister, Konrad", self.TestOptions).getValues()), set(("Meister, K.", "Meister, Konrad")))

    unittest.main()
