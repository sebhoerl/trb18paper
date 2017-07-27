#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import codecs
import sys

from .strings import formatKeyValueEntry, keyValueEntryRegex
from .file import getTempFileName, safeRename

from .six import u, text_type, binary_type

class Entity(object):
    def __init__(self, options):
        self._options = options

    class _IterateFile(object):
        def __init__(self, e):
            self._e = e

        STATE_PRE = 0
        STATE_IN = 1
        STATE_POST = 2

        def getState(self):
            return self.state

        def getGenerator(self):
            e = self._e
            startingPointRegex = re.compile("^%% %s" % re.escape(e.getSeparator()))
            with codecs.open(e._options.fileName, "r", e._options.encoding) as file:
                self.state = self.STATE_PRE
                
                for line in file:
                    yield line
                    if not (startingPointRegex.match(line) is None):
                        break

                self.state = self.STATE_IN
            
                for line in file:
                    yield line
                    break

                retVal = None
                endingPointRegex = re.compile("^%%")
                for line in file:
                    if not ((yield line) is None):
                        break

                    if not (endingPointRegex.match(line) is None):
                        break

                self.state = self.STATE_POST

                for line in file:
                    yield line


    def _findEntryInFile(self):
        findEntryValues = self.getValues()
        
        if not hasattr(findEntryValues, '__iter__'):
            findEntryValues = [findEntryValues]
            
        i = self._IterateFile(self)
        g = i.getGenerator()
        for decodedLine in g:
            entryMatch = keyValueEntryRegex.match(decodedLine)
            if entryMatch is None:
                continue

            currentEntryValue = entryMatch.group(2)

            for findEntryValue in findEntryValues:
                if currentEntryValue == findEntryValue:
                    return (entryMatch.group(1), currentEntryValue)

        return (None, None)


    def _findKeyInFile(self, key):
        i = self._IterateFile(self)
        g = i.getGenerator()
        for decodedLine in g:
            entryMatch = keyValueEntryRegex.match(decodedLine)
            if entryMatch is None:
                continue

            currentKey = entryMatch.group(1)

            if currentKey == key:
                return entryMatch.group(2)

        return None


    def _lessThan(self, a, b):
        return a < b


    def _equals(self, a, b):
        return a == b


    def _insertEntryIntoFile(self):
        keyGenerator = self.getKeyGenerator()
        value = self.getValue()
        
        key = next(keyGenerator)
        while self._findKeyInFile(key):
            key = next(keyGenerator)

        tempFileName = getTempFileName(self._options.fileName)

        with codecs.open(tempFileName, "w", self._options.encoding) as tempFile:
            i = self._IterateFile(self)
            g = i.getGenerator()


            # copy file until starting point:
            for decodedLine in g:
                tempFile.write(decodedLine)
                if i.getState() != i.STATE_PRE:
                    break
                
            # copy file until point of insertion of the current key
            # lookaheadBuffer stores contents that is not copied yet
            assert i.getState() == i.STATE_IN
            lookaheadBuffer = ""
            for decodedLine in g:
                entryMatch = keyValueEntryRegex.match(decodedLine)

                # non-matching entries are added to the lookahead buffer
                if entryMatch is None:
                    lookaheadBuffer += decodedLine
                    
                    if i.getState() != i.STATE_IN:
                        # Insert new entity after the previously inserted entity:
                        entityLine = formatKeyValueEntry(key, value, self.getKeyPartWidth())
                        lookaheadBuffer = entityLine + lookaheadBuffer
                        break
                    
                    continue
                
                (currentEntryKey, currentEntryValue) = entryMatch.groups()

                # insertion point found?
                if self._lessThan(key, currentEntryKey):
                    # If first char of the current key is the same as the desired key,
                    # insert entity before the current line.  To achieve that, append
                    # entity to lookahead buffer.
                    # If, on the other hand, the first chars differ, prepend entity to
                    # lookahead buffer.  The new entity is inserted before the lookahead
                    # buffer, which means adding the entity just after the previously
                    # inserted entity.
                    entityLine = formatKeyValueEntry(key, value, self.getKeyPartWidth())
                    if key[0] == currentEntryKey[0]:
                        lookaheadBuffer += entityLine
                    else:
                        lookaheadBuffer = entityLine + lookaheadBuffer

                    # Add current line to lookahead buffer in order to write it when
                    # flushing.
                    lookaheadBuffer += decodedLine
                    break

                # duplicate key found? we expect a unique key
                assert key != currentEntryKey

                # flush lookahead buffer
                if len(lookaheadBuffer) != 0:
                    tempFile.write(lookaheadBuffer)
                    lookaheadBuffer = ""

                tempFile.write(decodedLine)

            # flush lookahead buffer a last time, writing the entity to be inserted:
            if len(lookaheadBuffer) != 0:
                tempFile.write(lookaheadBuffer)
                lookaheadBuffer = ""

            # copy rest of file:
            for decodedLine in g:
                tempFile.write(decodedLine)

        safeRename(tempFileName, self._options.fileName)
        return key

    def sort(self):
        tempFileName = getTempFileName(self._options.fileName)

        with codecs.open(tempFileName, "w", self._options.encoding) as tempFile:
            i = self._IterateFile(self)
            g = i.getGenerator()

            # copy file until starting point:
            for decodedLine in g:
                tempFile.write(decodedLine)
                if i.getState() != i.STATE_PRE:
                    break
                
            # sort entities in "our" part
            assert i.getState() == i.STATE_IN
            previousEntity = None
            changed = False
            for decodedLine in g:
                entryMatch = keyValueEntryRegex.match(decodedLine)

                # directly write non-entities
                if entryMatch is None:
                    if previousEntity:
                        tempFile.write(previousEntity)
                        previousEntity = None
                    tempFile.write(decodedLine)

                    if i.getState() != i.STATE_IN:
                        break
                    
                    continue

                # locally sort entities:
                if previousEntity:
                    if self._lessThan(previousEntity, decodedLine):
                        tempFile.write(previousEntity)
                        previousEntity = decodedLine
                    elif self._equals(previousEntity, decodedLine):
                        if not changed:
                            print("Change detected: %s == %s", (previousEntity, decodedLine))
                        changed = True
                    else:
                        tempFile.write(decodedLine)
                        if not changed:
                            print("Change detected: %s > %s", (previousEntity, decodedLine))
                        changed = True
                else:
                    previousEntity = decodedLine

            # just to be sure
            if previousEntity:
                tempFile.write(previousEntity)
                previousEntity = None

            # copy rest of file:
            for decodedLine in g:
                tempFile.write(decodedLine)

        safeRename(tempFileName, self._options.fileName)
        return changed


    def add(self):
        self.checkAndFixValue()

        if not self._options.append:
            (currentKey, currentEntity) = self._findEntryInFile()
            if not (currentKey is None):
                raise Exception("Entity already in database: %s=\"%s\"." % (currentKey, currentEntity))
            
        return self._insertEntryIntoFile()


    def getKeyPartWidth(self):
        return 0


    @staticmethod
    def getTerminationShortcut():
        if sys.platform == "win32":
            return "<Ctrl+Z Enter>"
        else:
            return "<Ctrl+D>"


    @classmethod
    def process(entityType, args, options, stdin_message):
        if options.sortOnly:
            myEntity = entityType("", options)

            while myEntity.sort():
                pass
            return

        if not args:
            args = ["-"]
            
        for fileName in args:
            if fileName == "-":
                sys.stderr.write("%s\n%s\n" % (stdin_message,
                                               "Type %s to finish." % Entity.getTerminationShortcut()))
                fileStream = sys.stdin
            else:
                fileStream = codecs.open(fileName, mode="rU", encoding=options.encoding, buffering=0)

            while True:
                entityValue = fileStream.readline()
                if entityValue == "":
                    break
                if entityValue is None:
                    break
                entityValue = entityValue[:-1]
                if type(entityValue) is binary_type:
                    entityValue = entityValue.decode("utf8")

                entityValue = entityValue.strip()
                myEntity = entityType(entityValue, options)
                try:
                    authorKey = myEntity.add()
                except Exception as e:
                    print(type(entityValue))
                    sys.stderr.write(codecs.encode(u("\"%s\": not added: %s\n") % (entityValue, e), "utf8").decode(sys.stderr.encoding, "ignore"))
                else:
                    sys.stderr.write(codecs.encode(u("%s=\"%s\": added\n") % (authorKey, myEntity.getValue()), "utf8").decode(sys.stderr.encoding, "ignore"))

            fileStream.close()


if __name__=='__main__':
    import unittest
    import os.path
    from . import strings
    class TestIterateFile(unittest.TestCase):
        _contents = u"""
ignore
ignore

%%%%%
% Starting point
%%%%%
analyze

% comment

both
%%%%%
% Another starting point
%%%%%
ignore
"""

        _f = "f"
        _re1 = re.compile("(?:|ignore|both|(?:\%.*))$")
        _re2 = re.compile("(?:|analyze|both|\%.*)$")
        _re3 = re.compile("\% ")
        
        def setUp(self):
            with codecs.open(self._f, "w", "latin1") as f:
                f.write(self._contents.replace('\n', strings._nativeEol))
            
        def test_iterateFile(self):
            class TestEntity(Entity):
                def __init__(self, options):
                    super(TestEntity, self).__init__(options)

                def getSeparator(self):
                    return "Starting point"

            class TestOptions:
                pass

            TestOptions.encoding = "latin1"
            TestOptions.fileName = self._f

            e = TestEntity(TestOptions)
            i = e._IterateFile(e)

            for decodedLine in i.getGenerator():
                if i.getState() == i.STATE_PRE:
                    #sys.stderr.write(decodedLine)
                    decodedLine = decodedLine.rstrip()
                    self.assertTrue(self._re1.match(decodedLine))
                elif i.getState() == i.STATE_IN:
                    #sys.stderr.write(decodedLine)
                    decodedLine = decodedLine.rstrip()
                    self.assertTrue(self._re2.match(decodedLine))
                    if self._re3.match(decodedLine):
                        retVal = "myTestValue"
                elif i.getState() == i.STATE_POST:
                    #sys.stderr.write(decodedLine)
                    decodedLine = decodedLine.rstrip()
                    self.assertTrue(self._re1.match(decodedLine))
                else:
                    self.assertTrue(False)

            self.assertEqual(retVal, "myTestValue")

        def tearDown(self):
            if os.path.exists(self._f):
                os.unlink(self._f)

    class TestFindEntryInFile(unittest.TestCase):
        _contents = u"""
ignore
keyOne	valueOne

%%%%%
% Starting point
%%%%%
keyTwo	valueTwo

% comment

both
%%%%%
% Another starting point
%%%%%
keyThree	valueThree
ignore
"""

        _f = "f"
        
        def setUp(self):
            with codecs.open(self._f, "w", "latin1") as f:
                f.write(self._contents.replace('\n', strings._nativeEol))
            
        def test_findEntryInFile(self):
            class TestEntity(Entity):
                def __init__(self, options):
                    super(TestEntity, self).__init__(options)

                def getSeparator(self):
                    return "Starting point"

                def getValues(self):
                    return [self._value]

            class TestOptions:
                pass

            TestOptions.encoding = "latin1"
            TestOptions.fileName = self._f

            e = TestEntity(TestOptions)

            e._value = "valueOne"
            self.assertEqual(e._findEntryInFile(), ("keyOne", "valueOne"))
            e._value = "valueTwo"
            self.assertEqual(e._findEntryInFile(), ("keyTwo", "valueTwo"))
            e._value = "valueThree"
            self.assertEqual(e._findEntryInFile(), ("keyThree", "valueThree"))
            e._value = "valueFour"
            self.assertEqual(e._findEntryInFile(), (None, None))

        def tearDown(self):
            if os.path.exists(self._f):
                os.unlink(self._f)

    class TestInsertEntryIntoFile(unittest.TestCase):
        _contents = u"""
ignore
keyOne	valueOne

%%%%%
% Starting point
%%%%%
keyB	valueB
keyD	valueD

leyG	valueG

% comment

both
%%%%%
% Another starting point
%%%%%
keyThree	valueThree
ignore
"""

        _desiredContents = u"""
ignore
keyOne	valueOne

%%%%%
% Starting point
%%%%%
keyA	valueA
keyB	valueB
keyC	valueC
keyD	valueD
keyE	valueE
keyThreeQ	anotherValueThree

leyF	valueF
leyG	valueG
leyH	valueH

% comment

both
%%%%%
% Another starting point
%%%%%
keyThree	valueThree
ignore
"""

        _f = "f"
        
        def setUp(self):
            with codecs.open(self._f, "w", "latin1") as f:
                f.write(self._contents.replace('\n', strings._nativeEol))
            
        def test_insertEntryIntoFile(self):
            class TestEntity(Entity):
                def __init__(self, options):
                    super(TestEntity, self).__init__(options)

                def getSeparator(self):
                    return "Starting point"

                def getKeyGenerator(self):
                    yield self._key
                    yield self._key + 'Q'

                def getValue(self):
                    return self._value

            class TestOptions:
                pass

            TestOptions.encoding = "latin1"
            TestOptions.fileName = self._f

            keyValuePairs = \
                [("key%s" % k, "value%s" % k) for k in ["A", "C", "E"]] + \
                [("ley%s" % k, "value%s" % k) for k in ["F", "H"]]
                
            keyValuePairs += [("keyThree", "anotherValueThree")]

            for kv in keyValuePairs:
                e = TestEntity(TestOptions)
                (e._key, e._value) = kv
                e._insertEntryIntoFile()

            with codecs.open(self._f, "r", "latin1") as f:
                contents = f.read()

            #print contents
            #print self._desiredContents
            self.assertEqual(contents, self._desiredContents.replace('\n', strings._nativeEol))

        def tearDown(self):
            if os.path.exists(self._f):
                os.unlink(self._f)

    unittest.main()
