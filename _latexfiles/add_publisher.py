#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import codecs

from ivt_bibtools.publisher import Publisher as MyEntityType

if __name__=='__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [options] [new publisher file] ...",
                          epilog="The publisher file(s) should contain one publisher per line in the format publisher=Key.  "
                                 "Empty lines are allowed.  "
                                 "If no publisher file is given, the program reads the list of publishers from standard input.  "
                                 "In this case, type %s to finish.  " % MyEntityType.getTerminationShortcut())
    parser.add_option("-f", "--file-name", action="store", type="string", default="bibs/publisher.txt", dest="fileName", help="Name of definition file with list of aliases.  Default: %default")
    parser.add_option("-e", "--encoding", action="store", type="string", default="latin1", dest="encoding", help="Encoding for definition file.  Default: %default")
    parser.add_option("-a", "--append", action="store_true", dest="append", help="Create new entry even if a similar entry exists.")
    parser.add_option("-s", "--sort-only", action="store_true", dest="sortOnly", help="Only sort publishers and exit.")

    (options, args) = parser.parse_args()
    MyEntityType.process(args, options, "Please input publisher names, one per line, in the format Publisher=Key")
