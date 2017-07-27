#!/usr/bin/python
# -*- coding: utf8 -*-

import unicodedata
import re
import sys

from .six import u

if sys.platform == "win32":
    _nativeEol = '\r\n'
else:
    # Yes, LF is the native EOL even on Mac OS X. CR is just for
    # Mac OS <=9 (a.k.a. "Mac Classic")
    _nativeEol = '\n'

def toAscii(s):
    s = s.replace(u("\xe4"), "ae")
    s = s.replace(u("\xf6"), "oe")
    s = s.replace(u("\xfc"), "ue")
    s = s.replace(u("\xc4"), "Ae")
    s = s.replace(u("\xd6"), "Oe")
    s = s.replace(u("\xdc"), "Ue")
    s = s.replace(u("\xdf"), "ss")
    decoded = unicodedata.normalize("NFKD", s)
    return decoded.encode("ascii", "replace").decode("ascii", "replace").replace("?", "")

def toIdentifier(s):
    s = toAscii(s)
    return re.sub("[^a-zA-Z]", "", s)
    
keyValueEntryRegex = re.compile("^([^\t]+)\t(.*)$")

def formatKeyValueEntry(key, value, width=0):
    return key + "\t" + value + _nativeEol

if __name__=='__main__':
    import unittest
    class Test(unittest.TestCase):
        def test_toAscii(self):
            self.assertEqual(toAscii(u"Kirill"), "Kirill")
            self.assertEqual(toAscii(u"Müller"), "Mueller")
            self.assertEqual(toAscii(u"Léfèbvre"), "Lefebvre")
            self.assertEqual(toAscii(u"äöüÄÖÜß"), "aeoeueAeOeUess")
            self.assertEqual(toAscii(u"áàâéèêíìîóòôúùû"), "aaaeeeiiiooouuu")

        def test_toIdentifier(self):
            self.assertEqual(toIdentifier(u"O'Toole"), "OToole")

        def test_formatKeyValueEntry(self):
            self.assertEqual(formatKeyValueEntry("key", "value"), "key\tvalue%s" % _nativeEol)
            self.assertEqual(formatKeyValueEntry("key", "value", 15), "key\tvalue%s" % _nativeEol)
            self.assertTrue(keyValueEntryRegex.match(formatKeyValueEntry("key", "value")))
            self.assertTrue(keyValueEntryRegex.match(formatKeyValueEntry("key", "value", 53)))

    unittest.main()

