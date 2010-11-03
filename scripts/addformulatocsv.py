import csvutil, sys, optparse

def parseArgs(args):
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", default='\t')
    parser.add_option("-f", "--formula", dest="formula", default='\t')
    parser.add_option("-t", "--formula-column-title", dest="columnTitle", default='\t')
    (options, args) = parser.parse_args()
    return options, args

if __name__ == '__main__':
    options, args = parseArgs(sys.argv[1:])
    headerFields, rows = csvutil.getHeaderAndContentsAsDictionaries(delimiter=options.delimiter)
    newHeaderFields = headerFields[:]
    newHeaderFields.append(options.columnTitle)
    for i in range(1, len(rows) + 1):
        rows[i-1][options.columnTitle] = options.formula.replace('_NNNN', str(i+1))
        #print rows[i-1]
    csvutil.writeCSVContentsFromDictionaries(rows, fieldnames=newHeaderFields, delimiter=options.delimiter)
