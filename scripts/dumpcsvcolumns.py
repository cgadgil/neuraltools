from csvutil import *

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
