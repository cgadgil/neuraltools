#!/bin/env python

import sys, os, csvutil, optparse, StringIO

def parseArgs(args=sys.argv[1:]):
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", default='\t')
    parser.add_option("-c", "--column-name", dest="columnName")
    (options, args) = parser.parse_args()
    return options, args

if __name__ == '__main__':
    options, args = parseArgs()
    columnNameToRemove = options.columnName
    delimiter = options.delimiter
    fd = StringIO.StringIO()
    deletedContents = csvutil.deleteColumn(columnNameToRemove, fdout=fd, delimiter=delimiter)
    fd.close()
    print deletedContents
