import StringIO, sys, os, urllib2, httplib, multiprocessing, re, time, optparse, datetime
#from xml.sax.saxutils import escape
from BeautifulSoup import BeautifulSoup

balanceSheetFieldList = ['Period End Date', 'Stmt Source Date', 'Cash and Short Term Investments', 'Cash & Equivalents', 'Total Receivables, Net', 'Total Inventory', 'Prepaid Expenses', 'Other Current Assets, Total', 'Total Current Assets', 'Property/Plant/Equipment, Total - Net', 'Goodwill, Net', 'Intangibles, Net', 'Long Term Investments', 'Note Receivable - Long Term', 'Other Long Term Assets, Total', 'Other Assets, Total', 'Total Assets', 'Accounts Payable', 'Payable/Accrued', 'Accrued Expenses', 'Notes Payable/Short Term Debt', 'Current Port. of LT Debt/Capital Leases', 'Other Current Liabilities, Total', 'Total Current Liabilities', 'Total Long Term Debt', 'Deferred Income Tax', 'Minority Interest', 'Other Liabilities, Total', 'Total Liabilities', 'Redeemable Preferred Stock', 'Preferred Stock - Non Redeemable, Net', 'Common Stock', 'Retained Earnings (Accumulated Deficit)', 'Other Equity, Total', 'Total Equity', 'Total Common Shares Outstanding', 'Total Preferred Shares Outstanding']

incomeStatementFieldList=['Period End Date', 'Stmt Source Date', 'Revenue', 'Total Revenue', 'Cost of Revenue, Total', 'Gross Profit', 'Selling/General/Administrative Expenses, Total', 'Research & Development', 'Depreciation/Amortization', 'Interest Expense (Income), Net Operating', 'Unusual Expense (Income)', 'Other Operating Expenses, Total', 'Operating Income', 'Interest Income (Expense), Net Non-Operating', 'Gain (Loss) on Sale of Assets', 'Other, Net', 'Income Before Tax', 'Income Tax - Total', 'Income After Tax', 'Minority Interest', 'Equity In Affiliates', 'U.S. GAAP Adjustment', 'Net Income Before Extra. Items', 'Total Extraordinary Items', 'Net Income']

cashFlowStatementFieldList = ['Period End Date', 'Stmt Source Date', 'Net Income/Starting Line', 'Depreciation/Depletion', 'Amortization', 'Non-Cash Items', 'Other Non-Cash Items', 'Changes in Working Capital', 'Cash from Operating Activities', 'Capital Expenditures', 'Purchase of Fixed Assets', 'Other Investing Cash Flow Items, Total', 'Cash from Investing Activities', 'Financing Cash Flow Items', 'Other Financing Cash Flow', 'Total Cash Dividends Paid', 'Issuance (Retirement) of Stock, Net', 'Issuance (Retirement) of Debt, Net', 'Cash from Financing Activities', 'Foreign Exchange Effects', 'Net Change in Cash', 'Net Cash - Beginning Balance', 'Net Cash - Ending Balance']

def parseArgs(args):
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tag", dest="tag", default='latest')
    parser.add_option("-o", "--out-dir", dest="outdir", default='.')
    (options, args) = parser.parse_args()
    return options, args

def getStatementField(xmlDocument, fieldName):
    r = re.compile('^' + re.escape(fieldName), re.I)
    return xmlDocument.findAll(text=fieldName)

def getHistoricalQuote(symbol, dateStr, tryDays=10):
    # dateStr in %m/%d/%Y format
    #"http://finance.yahoo.com/q/hp?s=GE&a=05&b=2&c=2010&d=05&e=2&f=2010&g=d"
    #"http://ichart.finance.yahoo.com/table.csv?s=GE&a=05&b=2&c=2010&d=05&e=2&f=2010&g=d&ignore=.csv"
    for i in range(tryDays):
        try:
            #import pdb
            #pdb.set_trace()
            dt = datetime.datetime.strptime(dateStr, '%m/%d/%Y')
            dt = dt - datetime.timedelta(1*i)
            url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv" % (symbol, dt.month-1, dt.day, dt.year, dt.month-1, dt.day, dt.year)
            fd = urllib2.urlopen(url)
            theCSV = fd.read()
            thePrice = theCSV.split("\n")[1].split(",")[4]
            fd.close()
            #print thePrice
            return thePrice
        except:
            print "getHistoricalQuote for symbol [%s]" % (symbol,),
            print sys.exc_info()
    return "0"

def getHtmlSoup(url):
    fd = urllib2.urlopen(url)
    r = fd.read()
    fd.close()
    return BeautifulSoup(r)

def getSummaryData(symbol):
    url = 'http://finance.yahoo.com/q/ks?s=' + symbol
    x = getHtmlSoup(url)
    theLow = x.find(text=re.compile('52-Week Low')).parent.parent.contents[1].text
    theHigh = x.find(text=re.compile('52-Week High')).parent.parent.contents[1].text
    theBeta = x.find(text=re.compile('Beta:')).parent.parent.contents[1].text
    return {'summary-52-Wk High': theHigh, 'summary-52-Wk Low': theLow, 'Beta': theBeta }

def getSummaryData_old(symbol):
    url = 'http://investing.money.msn.com/investments/stock-price?symbol=US%3a' + symbol
    x = getHtmlSoup(url)
    theLow = x.find(text=re.compile('52-Wk Low')).parent.parent.parent.contents[3].span.text
    theHigh = x.find(text=re.compile('52-Wk High')).parent.parent.parent.contents[3].span.text
    return {'summary-52-Wk High': theHigh, 'summary-52-Wk Low': theLow }

def getBalanceSheet(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=Balance&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getIncomeStatement(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=Income&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getCashFlowStatement(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=CashFlow&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getStatementDictionary(symbol, xmlDocument, period, fieldList, statementType, label, tag):
    theDict = {}
    for i in fieldList:
        #print i
        #i2 = re.sub("[ &\(\)/,\']", "__", i).lower()
        theNode = xmlDocument.find(text=i)
        if not theNode:
            raise Exception('Failed to find field [%s] for symbol[%s] and statement type [%s]' % (i, symbol, statementType))
        theTR = theNode.parent.parent
        while theTR.name != "tr":
            theTR = theTR.parent
        theDict[i] = theTR.contents[period].text
        if i == 'Stmt Source Date':
            theDict['price'] = getHistoricalQuote(symbol, theTR.contents[period].text)
            #print theStr
    #theStr = theStr + "</%s>" % (statementType,)
    #theDict["statement-type"] = statementType
    theDict["label"] = label
    theDict["tag"] = tag
    theDict["period"] = str(period)
    theDict["symbol"] = symbol
    theDict.update(getSummaryData(symbol))
    theDict["latest-price"] = getHistoricalQuote(symbol, datetime.date.today().strftime("%m/%d/%Y"))
    return theDict

def getXmlString_old(symbol, xmlDocument, period, fieldList, statementType, label, tag):
    theStr = "<%s>" % (statementType,)
    theStr = theStr + "<time-stamp>" + str(label) + "</time-stamp>"
    theStr = theStr + "<tag>" + tag + "</tag>"
    theStr = theStr + "<symbol>" + symbol + "</symbol>"
    theStr = theStr + "<period>" + str(period) + "</period>"
    for i in fieldList:
        #print i
        i2 = re.sub("[ &\(\)/,\']", "__", i).lower()
        theNode = xmlDocument.find(text=i)
        if not theNode:
            raise Exception('Failed to find field [%s] for symbol[%s] and statement type [%s]' % (i, symbol, statementType))
        theTR = theNode.parent.parent
        while theTR.name != "tr":
            theTR = theTR.parent
        theStr = theStr + "<%s>%s</%s>" % (i2, theTR.contents[period].text, i2)
        if i == 'Stmt Source Date':
            theStr = theStr + "<latest-price>" + getHistoricalQuote(symbol, theTR.contents[period].text) + "</latest-price>"
            #print theStr
    theStr = theStr + "</%s>" % (statementType,)
    return theStr

def getStatements(symbol, tag):
    "get statements for the last 5 periods. returns a tuple containing 3 lists - the balance sheets, the cash flows and the income statements"
    label = str(time.time())
    bs = getBalanceSheet(symbol)
    cfs = getCashFlowStatement(symbol)
    incS = getIncomeStatement(symbol)
    bss = []
    cfss = []
    incss = []
    for i in range(1, 6):
        bss.append(getStatementDictionary(symbol, bs, i, balanceSheetFieldList, "balance-sheet", label, tag))
        cfss.append(getStatementDictionary(symbol, cfs, i, cashFlowStatementFieldList, "cash-flow-statement", label, tag))
        incss.append(getStatementDictionary(symbol, incS, i, incomeStatementFieldList, "income-statement", label, tag))
    return (bss, cfss, incss)

def getXmlTags(dictContents):
    "get xml tags for given dictionary contents. the dictionary keys are mangled to be xml compliant"
    theStr = ""
    for i in dictContents.keys():
        i2 = re.sub("[ &\(\)/,\']", "__", i).lower()
        theStr = theStr + "<%s>%s</%s>" % (i2, dictContents[i].replace(",", ""), i2)
    return theStr

def writeFile(tag, fileName, contents, outdir):
    try:
        os.mkdir(outdir)
    except:
        print sys.exc_info()[1]
    fd = file(outdir + os.path.sep + fileName, "w")
    fd.write(contents)
    fd.close()

def writeStatements(symbol, tag, outdir):
    try:
        bss, cfss, incss = getStatements(symbol, tag)
        for i in range(5):
            xx = {}
            xx.update(bss[i])
            xx.update(cfss[i])
            xx.update(incss[i])
            theStr = getXmlTags(xx)
            writeFile(tag, symbol + "-data." + str(i+1) + ".xml", "<data>%s</data>" % (theStr), outdir)
        #writeFile(tag, symbol + "-balance-sheets.xml", "<balance-sheets>" + "\n".join(bss) + "</balance-sheets>", outdir)
        #writeFile(tag, symbol + "-income-statement.xml", "<income-statements>" + "\n".join(incss) + "</income-statements>", outdir)
        #writeFile(tag, symbol + "-cash-flows.xml", "<cash-flows>" + "\n".join(cfss) + "</cash-flows>", outdir)
    except:
        print "error processing [%s], ignoring" % (symbol,) + str(sys.exc_info())

def ww(*k):
    print k[0]
    apply(writeStatements, k[0])

def processSymbols(symbolList, tag, outdir):
    pool = multiprocessing.Pool(processes=5)
    #map(ww, [(i, tag, outdir) for i in symbolList])
    return filter(None, pool.map(ww, [(i, tag, outdir) for i in symbolList]))

if __name__ == '__main__':
    opts, args = parseArgs(sys.argv[1:])
    #writeStatements(args[0], opts.tag, opts.outdir)
    processSymbols(args, opts.tag, opts.outdir)
