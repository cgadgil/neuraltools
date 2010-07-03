import sys, json, urllib2, uuid, sqlite3, csv, StringIO

#T1 = (Current Assets-Current Liabilities) / Total Assets
#T2 = Retained Earnings / Total Assets
#T3 = Earnings Before Interest and Taxes / Total Assets
#T4 = Book Value of Equity / Total Liabilities
#T5 = Sales/ Total Assets

def getAllTs(balanceSheet, cashFlow, income):
    numShares = float(balanceSheet['Total Common Shares Outstanding'])
    #closePrice = float(balanceSheet['Historical-Quote'].split('|')[1].split(',')[4])
    closePrice = float(balanceSheet['Historical-Quote'])
    marketCap = numShares * closePrice
    t1 = (float(balanceSheet['Total Current Assets']) - float(balanceSheet['Total Current Liabilities'])) / float(balanceSheet['Total Assets'])
    t2 = float(balanceSheet['Retained Earnings (Accumulated Deficit)']) / float(balanceSheet['Total Assets'])
    t3 = float(income['Operating Income']) / float(balanceSheet['Total Assets'])
    t4 = marketCap / float(balanceSheet['Total Liabilities'])
    bookValueOfEquity = float(balanceSheet['Total Equity'])
    t4prime = bookValueOfEquity / float(balanceSheet['Total Liabilities'])
    t5 = float(income['Total Revenue']) / float(balanceSheet['Total Assets'])
    #print balanceSheet['Historical-Quote']
    return {'X1': t1, 'X2': t2, 'X3': t3, 'X4': t4, 'X4prime':t4prime, 'X5': t5}

def getZScore(t1, t2, t3, t4, t5):
    #Z = 1.2T1 + 1.4T2 + 3.3T3 + 0.6T4 + 0.999T5
    z = 1.2*t1 + 1.4*t2 + 3.3*t3 + 0.6*t4 + 0.999*t5
    return z

def getZPrimeScore(t1, t2, t3, t4prime, t5):
    #Z' = 0.717T1 + 0.847T2 + 3.107T3 + 0.420T4 + 0.998T5
    z = 0.717 * t1 + 0.847*t2 + 3.107*t3 + 0.42*t4prime + 0.998*t5
    return z

def getZDoublePrimeScore(t1, t2, t3, t4prime, t5):
    #Z'' = 6.56T1 + 3.26T2 + 6.72T3 + 1.05T4
    z = 6.56*t1 + 3.26*t2 + 6.72*t3 + 1.05*t4prime
    return z

def getDataForSymbol(symbol, periodType):
    x = urllib2.urlopen("http://localhost:8080/fundamental/fundie/%s/%s" % (symbol, periodType))
    xxx = x.read()
    yyy = json.loads(xxx, strict=False)
    yyy = yyy['data']
    apply(getZScore, getAllTs(yyy[0][1], yyy[1][1], yyy[2][1]))

def dummy():
    #[apply(getZScore, j) for j in [getAllTs(yyy['data'][0][i], yyy['data'][1][i], yyy['data'][2][i]) for i in range(5)]]
    #[1.1069052153081427, 1.3905203998912641, 1.7963183867143975, 2.37862843044178, 2.2720216794383243]
    pass

def generateInsertData(symbol, periodType, generatedId, statementType, statements):
    insertValues = []
    for periodSetNum in range(len(statements)):
        singleStatement = statements[periodSetNum]
        for propertyName in singleStatement.keys():
            #sqlStr = 'insert into dataset (symbol, periodtype, generatedid, periodsetnum, statementtype, propertyname, propertyvalue) values (?, ?, ?, ?, ?, ?, ?)'
            propertyValue = singleStatement[propertyName]
            insertValues.append((symbol, periodType, generatedId, periodSetNum, statementType, propertyName, propertyValue))
    return insertValues

def storeInDB(dataSet):
    #[u'symbol', u'period-type', u'data', u'generated-id']
    #conn = sqlite3.connect('chetan.dataset.sqlite3.db')
    fileName = str(uuid.uuid4()) + '.db'
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    # Create table
    c.execute('create table "dataset" (symbol varchar(256), periodtype varchar(256), generatedid varchar(256), periodsetnum integer, statementtype varchar(256), propertyname varchar(256), propertyvalue varchar(256))')
    # Insert a row of data
    symbol = dataSet['symbol']
    periodType = dataSet['period-type']
    generatedId = dataSet['generated-id']
    balanceSheetDataSets = dataSet['data'][0]
    cashFlowDataSets = dataSet['data'][1]
    incomeSheetDataSets = dataSet['data'][2]
    #c.execute('insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)')
    sqlStr = 'insert into dataset (symbol, periodtype, generatedid, periodsetnum, statementtype, propertyname, propertyvalue) values (?, ?, ?, ?, ?, ?, ?)'
    c.executemany(sqlStr, generateInsertData(symbol, periodType, generatedId, 'BALANCE-SHEET', balanceSheetDataSets))
    c.executemany(sqlStr, generateInsertData(symbol, periodType, generatedId, 'CASH-FLOW', cashFlowDataSets))
    c.executemany(sqlStr, generateInsertData(symbol, periodType, generatedId, 'INCOME', incomeSheetDataSets))
    # Save (commit) the changes
    conn.commit()
    # We can also close the cursor if we are done with it
    c.close()
    conn.close()
    conn = sqlite3.connect(fileName)
    dumpIter = conn.iterdump()
    lines = [line for line in dumpIter]
    conn.close()
    print symbol
    return lines

def getDataSetForSymbol(symbol, periodType):
    fd = urllib2.urlopen("http://localhost:8080/fundamental/fundie/%s/%s" % (symbol, periodType))
    jsonStr = fd.read()
    fd.close()
    dataSet = json.loads(jsonStr)
    return dataSet

def storeDataForSymbol(symbol, periodType):
    dataSet = getDataSetForSymbol(symbol, periodType)
    return storeInDB(dataSet)

def addValueToDict(dictObj, key, value):
    dictObj[key] = value

def getCommonDataFields(dataSet):
    # Balance Sheet
    #
    # 'Total Common Shares Outstanding', 'Historical-Quote', 'Total Current Assets', 'Total Assets','Retained Earnings (Accumulated Deficit)', 'Total Assets', 'Total Liabilities', 'Total Current Liabilities', 'Total Equity', 'Period End Date'
    balanceSheetFieldNames = ('Total Common Shares Outstanding', 'Historical-Quote', 'Total Current Assets', 'Total Assets','Retained Earnings (Accumulated Deficit)', 'Total Assets', 'Total Liabilities', 'Total Current Liabilities', 'Total Equity', 'Period End Date', 'Timestamp', 'Period', 'Period-Type', 'Cash & Equivalents')
    #
    # Income Statement
    #
    # 'Operating Income', 'Total Revenue', 'Gross Profit', 'Operating Income', 'Income Before Tax', 'Income After Tax', 'Net Income'
    incomeStatementFieldNames = ('Operating Income', 'Total Revenue', 'Gross Profit', 'Operating Income', 'Income Before Tax', 'Income After Tax', 'Net Income')
    #
    # Cash Flow Statement
    # 
    # 'Depreciation/Depletion', 'Amortization', 'Deferred Taxes', 'Cash from Operating Activities','Cash from Investing Activities', 'Cash from Financing Activities', 'Net Change in Cash'
    cashFlowFieldNames = ('Depreciation/Depletion', 'Amortization', 'Cash from Operating Activities','Cash from Investing Activities', 'Cash from Financing Activities', 'Net Change in Cash')
    symbol = dataSet['symbol']
    periodType = dataSet['period-type']
    generatedId = dataSet['generated-id']
    balanceSheetDataSets = dataSet['data'][0]
    cashFlowDataSets = dataSet['data'][1]
    incomeSheetDataSets = dataSet['data'][2]
    dataRows = []
    for i in range(5):
        # for each period
        combinedRow = {}
        balanceSheet = balanceSheetDataSets[i]
        cashFlow = cashFlowDataSets[i]
        income = incomeSheetDataSets[i]
        [addValueToDict(combinedRow, name, balanceSheet[name]) for name in balanceSheetFieldNames]
        [addValueToDict(combinedRow, name, cashFlow[name]) for name in cashFlowFieldNames]
        [addValueToDict(combinedRow, name, income[name]) for name in incomeStatementFieldNames]
        # Get all Ts - to calculate various Z Scores
        allTs = getAllTs(balanceSheet, cashFlow, income)
        t1, t2, t3, t4, t4prime, t5 = allTs['X1'], allTs['X2'], allTs['X3'], allTs['X4'], allTs['X4prime'], allTs['X5']
        zScore = getZScore(t1, t2, t3, t4, t5)
        zPrimeScore = getZPrimeScore(t1, t2, t3, t4prime, t5)
        zDoublePrimeScore = getZDoublePrimeScore(t1, t2, t3, t4prime, t5)
        combinedRow.update(allTs)
        combinedRow['zScore'] = zScore
        combinedRow['zPrimeScore'] = zPrimeScore
        combinedRow['zDoublePrimeScore'] = zDoublePrimeScore
        combinedRow['symbol'] = symbol
        combinedRow['generated-id'] = generatedId
        # Calculate performance ratio
        thePrice = float(combinedRow['Historical-Quote'])
        combinedRow['zScore-to-price'] = zScore / thePrice
        combinedRow['zPrimeScore-to-price'] = zPrimeScore / thePrice
        combinedRow['zDoublePrimeScore-to-price'] = zDoublePrimeScore / thePrice
        # pass
        # append the combined row
        dataRows.append(combinedRow)
    return dataRows

def getDataRowsForAllSymbols(symbolList, periodType):
    theStrFile = StringIO.StringIO()
    first = True
    for symbol in symbolList:
        try:
            d = getDataSetForSymbol(symbol, periodType)
            theDataRows = getCommonDataFields(d)
            fieldNames = theDataRows[0].keys()
            dw = csv.DictWriter(theStrFile, fieldNames, delimiter='\t')
            if first:
                fnd = {}
                for fn in fieldNames:
                    fnd[fn] = fn
                dw.writerow(fnd)
                first = False
            dw.writerows(theDataRows)
        except Exception as ex:
            print >> sys.stderr, ex
    return theStrFile.getvalue()

if __name__ == '__main__':
    periodType = sys.argv[1]
    symbolList = sys.argv[2:]
    print getDataRowsForAllSymbols(symbolList, periodType)
