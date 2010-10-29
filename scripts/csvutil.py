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
    print >> fd, delimiter.join(fieldnames)
    dw = csv.DictWriter(fd, fieldnames=fieldnames, delimiter=delimiter)
    dw.writerows(rows)

def deleteColumn(columnNameToRemove, fd=sys.stdout, delimiter='\t'):
    headerFields, rows = getHeaderAndContentsAsDictionaries(fd)
    headerFields.remove(columnNameToRemove)
    writeCSVContentsFromDictionaries(rows, headerFields, fd=fd, delimiter=delimiter)

if __name__ == '__main__':
    options, args = parseArgs(sys.argv[1:])
    headerFields, rows = getHeaderAndContentsAsDictionaries(sys.stdin, options.delimiter)
    fieldCount = len(headerFields)
    fieldPrefixes = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(1, fieldCount + 1):
        #print  i % 26, i / 26
        if i <= 26:
            prefix = fieldPrefixes[i % 26 - 1]
        else:
            prefix = fieldPrefixes[i / 26 - 1] + fieldPrefixes[i % 26 - 1]
        print "%s = %s" % (prefix, headerFields[i-1])
