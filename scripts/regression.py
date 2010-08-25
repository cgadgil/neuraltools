import httplib, urllib, json, sys, csv

def getRegressionResults(xData, yData):
    #xd = json.dumps([[1.0, 2.0, 3.0], [2.1, 4.4, 5.9], [3.6, 5.9, 8.2], [5.1, 9.3, 14.6]])
    #yd = json.dumps([11.2, 24.1, 29.2, 40.8])
    xd = json.dumps(xData)
    yd = json.dumps(yData)
    #print xData
    #print yData
    dd = urllib.urlencode({'xData': xd, 'yData': yd})
    params = dd
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost:8080")
    conn.request("POST", "/fundamental/regression", params, headers)
    return json.loads(conn.getresponse().read())

def getRegressionResultsWithIntercept(xData, yData):
    # expect data without dummy column in the xData
    xDataRowsWithDummy = []
    for row in xData:
        xDataRowsWithDummy.append([1.0] + row)
    return getRegressionResults(xDataRowsWithDummy, yData)


# getRegressionResults([[1.0, 1.0, 2.0, 3.0], [1.0, 2.1, 4.4, 5.9], [1.0, 3.6, 5.9, 8.2], [1.0, 5.1, 9.3, 14.6]], [11.2, 24.1, 29.2, 40.8])

#getRegressionResults([[1.0, 1.0, 2.0, 3.0], [1.0, 2.1, 4.4, 5.9], [1.0, 3.6, 5.9, 8.2], [1.0, 5.1, 9.3, 14.6], [1.0, 7.0, 11.0, 17.0]], [11.2, 24.1, 29.2, 40.8, 54.0])

def printCSVInputSummary():
    csvFile = csv.reader(sys.stdin, delimiter='\t')
    headerRow = csvFile.next()
    numColumns = len(headerRow)
    xData = []
    yData = []
    for row in csvFile:
        xData.append([float(i) for i in row[:numColumns-1]])
        yData.append(float(row[numColumns-1]))
    #print xData
    #print yData
    result = getRegressionResultsWithIntercept(xData, yData)['result']
    regressionParameters = result['regression-parameters']
    intercept = regressionParameters[0]
    coeffecients = regressionParameters[1:]
    print "[%s] = %f" % (headerRow[numColumns - 1], intercept,),
    for i in range(0, numColumns - 1):
        print " + ([%s] * %f)" % (headerRow[i], coeffecients[i]),
    print ""
    print "R Squared: %f" % (result['r-squared'])
    print "R Squared (Adj): %f" % (result['adjusted-r-squared'])
    print "Residuals: %s" % (str(result['residuals']))

if __name__ == '__main__':
    printCSVInputSummary()

    
    
