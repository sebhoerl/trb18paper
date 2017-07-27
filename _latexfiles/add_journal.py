#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import codecs

from ivt_bibtools.journal import Journal as MyEntityType

if __name__=='__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options] [new journals file] ...",
                          epilog="The journal file(s) should contain one journal per line in the format Journal=Key.  "
                                 "Empty lines are allowed.  "
                                 "If no journal file is given, the program reads the list of journals from standard input.  "
                                 "In this case, type %s to finish.  " % MyEntityType.getTerminationShortcut())
    parser.add_option("-f", "--file-name", action="store", type="string", default="bibs/journal.txt", dest="fileName", help="Name of definition file with list of aliases.  Default: %default")
    parser.add_option("-e", "--encoding", action="store", type="string", default="latin1", dest="encoding", help="Encoding for definition file.  Default: %default")
    parser.add_option("-a", "--append", action="store_true", dest="append", help="Create new entry even if a similar entry exists.")
    parser.add_option("-s", "--sort-only", action="store_true", dest="sortOnly", help="Only sort journals and exit.")

    (options, args) = parser.parse_args()
    MyEntityType.process(args, options, "Please input journal names, one per line, in the format Journal=Key")
