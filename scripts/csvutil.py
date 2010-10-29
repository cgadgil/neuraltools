#!/bin/env python

import sys, csv, optparse, cStringIO

def parseArgs(args):
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", default='\t')
    (options, args) = parser.parse_args()
    return options, args

def getHeaderAndContentsAsDictionaries(fd=sys.stdin, delimiter='\t'):
    contents = fd.read()
    contentsFileObj = cStringIO.StringIO(contents)
    dr = csv.DictReader(contentsFileObj, delimiter=delimiter)
    rows = [row for row in dr]
    fd2 = cStringIO.StringIO(contents)
    headerFields = fd2.readline().split(delimiter)
    fd2.close()
    return headerFields, rows

def writeCSVContentsFromDictionaries(rows, fieldnames, fd=sys.stdout, delimiter='\t'):
    fieldnames = [i.strip() for i in fieldnames]
    print >> fd, delimiter.join(fieldnames)
    dw = csv.DictWriter(fd, fieldnames=fieldnames, delimiter=delimiter)
    dw.writerows(rows)

def deleteColumn(columnNameToRemove, fd=sys.stdout, delimiter='\t'):
    headerFields, rows = getHeaderAndContentsAsDictionaries(fd)
    headerFields.remove(columnNameToRemove)
    writeCSVContentsFromDictionaries(rows, headerFields, fd=fd, delimiter=delimiter)

