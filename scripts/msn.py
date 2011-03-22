import StringIO, sys, os, urllib2, httplib, multiprocessing, re, time, optparse
#from xml.sax.saxutils import escape
from BeautifulSoup import BeautifulSoup

balanceSheetFieldList = ['Period End Date', 'Stmt Source Date', 'Cash and Short Term Investments', 'Cash & Equivalents', 'Total Receivables, Net', 'Total Inventory', 'Prepaid Expenses', 'Other Current Assets, Total', 'Total Current Assets', 'Property/Plant/Equipment, Total - Net', 'Goodwill, Net', 'Intangibles, Net', 'Long Term Investments', 'Note Receivable - Long Term', 'Other Long Term Assets, Total', 'Other Assets, Total', 'Total Assets', 'Accounts Payable', 'Payable/Accrued', 'Accrued Expenses', 'Notes Payable/Short Term Debt', 'Current Port. of LT Debt/Capital Leases', 'Other Current Liabilities, Total', 'Total Current Liabilities', 'Total Long Term Debt', 'Deferred Income Tax', 'Minority Interest', 'Other Liabilities, Total', 'Total Liabilities', 'Redeemable Preferred Stock', 'Preferred Stock - Non Redeemable, Net', 'Common Stock', 'Retained Earnings (Accumulated Deficit)', 'Other Equity, Total', 'Total Equity', 'Total Common Shares Outstanding', 'Total Preferred Shares Outstanding']

incomeStatementFieldList=['Period End Date', 'Stmt Source Date', 'Revenue', 'Total Revenue', 'Cost of Revenue, Total', 'Gross Profit', 'Selling/General/Administrative Expenses, Total', 'Research & Development', 'Depreciation/Amortization', 'Interest Expense (Income), Net Operating', 'Unusual Expense (Income)', 'Other Operating Expenses, Total', 'Operating Income', 'Interest Income (Expense), Net Non-Operating', 'Gain (Loss) on Sale of Assets', 'Other, Net', 'Income Before Tax', 'Income Tax - Total', 'Income After Tax', 'Minority Interest', 'Equity In Affiliates', 'U.S. GAAP Adjustment', 'Net Income Before Extra. Items', 'Total Extraordinary Items', 'Net Income']

cashFlowStatementFieldList = ['Period End Date', 'Stmt Source Date', 'Net Income/Starting Line', 'Depreciation/Depletion', 'Amortization', 'Non-Cash Items', 'Other Non-Cash Items', 'Changes in Working Capital', 'Cash from Operating Activities', 'Capital Expenditures', 'Purchase of Fixed Assets', 'Other Investing Cash Flow Items, Total', 'Acquisition of Business', 'Sale/Maturity of Investment', 'Cash from Investing Activities', 'Financing Cash Flow Items', 'Other Financing Cash Flow', 'Total Cash Dividends Paid', 'Issuance (Retirement) of Stock, Net', 'Issuance (Retirement) of Debt, Net', 'Cash from Financing Activities', 'Foreign Exchange Effects', 'Net Change in Cash', 'Net Cash - Beginning Balance', 'Net Cash - Ending Balance']

def parseArgs(args):
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tag", dest="tag", default='latest')
    parser.add_option("-o", "--out-dir", dest="outdir", default='.')
    (options, args) = parser.parse_args()
    return options, args

def getStatementField(xmlDocument, fieldName):
    r = re.compile('^' + re.escape(fieldName), re.I)
    return xmlDocument.findAll(text=fieldName)

def getHtmlSoup(url):
    fd = urllib2.urlopen(url)
    r = fd.read()
    fd.close()
    return BeautifulSoup(r)

def getBalanceSheet(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=Balance&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getIncomeStatement(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=Income&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getCashFlowStatement(symbol):
    url = "http://moneycentral.msn.com/investor/invsub/results/statemnt.aspx?lstStatement=CashFlow&stmtView=Ann&Symbol=US%3a" + symbol
    return getHtmlSoup(url)

def getXmlString(symbol, xmlDocument, period, fieldList, statementType, label, tag):
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
    theStr = theStr + "</%s>" % (statementType,)
    return theStr

def getStatements(symbol, tag):
    label = str(time.time())
    bs = getBalanceSheet(symbol)
    cfs = getCashFlowStatement(symbol)
    incS = getIncomeStatement(symbol)
    bss = []
    cfss = []
    incss = []
    for i in range(1, 6):
        bss.append(getXmlString(symbol, bs, i, balanceSheetFieldList, "balance-sheet", label, tag))
        cfss.append(getXmlString(symbol, cfs, i, cashFlowStatementFieldList, "cash-flow-statement", label, tag))
        incss.append(getXmlString(symbol, incS, 1, incomeStatementFieldList, "income-statement", label, tag))
    return (bss, cfss, incss)

def writeFile(tag, fileName, contents, outdir):
    try:
        os.mkdir(outdir)
    except:
        print sys.exc_info()[1]
    fd = file(outdir + os.path.sep + fileName, "w")
    fd.write(contents)
    fd.close()

def writeStatements(symbol, tag, outdir):
    bss, cfss, incss = getStatements(symbol, tag)
    writeFile(tag, symbol + "-balance-sheets.xml", "<balance-sheets>" + "\n".join(bss) + "</balance-sheets>", outdir)
    writeFile(tag, symbol + "-income-statement.xml", "<income-statements>" + "\n".join(incss) + "</income-statements>", outdir)
    writeFile(tag, symbol + "-cash-flows.xml", "<cash-flows>" + "\n".join(cfss) + "</cash-flows>", outdir)

def processSymbols(symbolList, tag, outdir):
    def f(symbol):
        writeStatements(symbol, tag, outdir)
    map(f, symbolList)

if __name__ == '__main__':
    opts, args = parseArgs(sys.argv[1:])
    #writeStatements(args[0], opts.tag, opts.outdir)
    processSymbols(args, opts.tag, opts.outdir)
