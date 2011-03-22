#/bin/env python

import StringIO, sys, os, urllib2, httplib, multiprocessing
#from xml.sax.saxutils import escape
import csvutil
from BeautifulSoup import BeautifulSoup

field_list_1 = ['PE Ratio - LTM', 'Market Capitalisation', 'Latest Shares Outstanding', 'Earnings pS (EPS)', 'Dividend pS (DPS)', 'Dividend Yield', 'Dividend Payout Ratio', 'Revenue per Employee', 'Effective Tax Rate', 'Float', 'Float as % of Shares Outstanding', 'Foreign Sales', 'Domestic Sales', 'Gross Profit Margin', 'EBITDA Margin', 'Pre-Tax Profit Margin', 'Assets Turnover', 'Return on Assets (ROA)', 'Return on Equity (ROE)', 'Return on Capital Invested (ROCI)', 'Current Ratio', 'Leverage Ratio (Assets/Equity)', 'Interest Cover', 'Total Debt/Equity (Gearing Ratio)', 'LT Debt/Total Capital', 'Working Capital pS', 'Cash pS', 'Book-Value pS', 'Tangible Book-Value pS', 'Cash Flow pS', 'Free Cash Flow pS']

field_list_2 = ['Price/Book Ratio', 'Price/Tangible Book Ratio', 'Price/Cash Flow', 'Price/Free Cash Flow', 'P/E as % of Industry Group', 'P/E as % of Sector Segment']

field_list_3 = ['Net Working Capital Ratio', 'Current Ratio', 'Quick Ratio (Acid Test)', 'Liquidity Ratio (Cash)', 'Receivables Turnover', 'Average Collection Period', 'Working Capital/Equity', 'Working Capital pS', 'Cash-Flow pS', 'Free Cash-Flow pS', "Altman's Z-Score Ratio", 'Financial Leverage Ratio (Assets/Equity)', 'Debt Ratio', 'Total Debt/Equity (Gearing Ratio)', 'LT Debt/Equity', 'LT Debt/Capital Invested', 'LT Debt/Total Liabilities', 'Interest Cover', 'Interest/Capital Invested', 'PQ Ratio', "Tobin's Q Ratio", 'Current P/E Ratio - LTM', 'Enterprise Value (EV)/EBITDA', 'Enterprise Value (EV)/Free Cash Flow', 'Dividend Yield', 'Price/Tangible Book Ratio - LTM', 'Price/Book Ratio - LTM', 'Price/Cash Flow Ratio', 'Price/Free Cash Flow Ratio - LTM', 'Price/Sales Ratio', 'P/E Ratio (1 month ago) - LTM', 'P/E Ratio (26 weeks ago) - LTM', 'P/E Ratio (52 weeks ago) - LTM', '5-Y High P/E Ratio', '5-Y Low P/E Ratio', '5-Y Average P/E Ratio', 'Current P/E Ratio as % of 5-Y Average P/E', 'P/E as % of Industry Group', 'P/E as % of Sector Segment', 'Current 12 Month Normalized P/E Ratio - LTM', 'LT Debt pS', 'Current Liabilities pS', 'Tangible Book Value pS - LTM', 'Book Value pS - LTM', 'Capital Invested pS', 'Cash pS - LTM', 'Cash Flow pS - LTM', 'Free Cash Flow pS - LTM', 'Earnings pS (EPS)', 'Free Cash Flow Margin', 'Free Cash Flow Margin 5YEAR AVG', 'Net Profit Margin', 'Net Profit Margin - 5YEAR AVRG.', 'Equity Productivity', 'Return on Equity (ROE)', 'Return on Equity (ROE) - 5YEAR AVRG.', 'Capital Invested Productivity', 'Return on Capital Invested (ROCI)', 'Return on Capital Invested (ROCI) - 5YEAR AVRG.', 'Assets Productivity', 'Return on Assets (ROA)', 'Return on Assets (ROA) - 5YEAR AVRG.', 'Gross Profit Margin', 'Gross Profit Margin - 5YEAR AVRG.', 'EBITDA Margin - LTM', 'EBIT Margin - LTM', 'Pre-Tax Profit Margin', 'Pre-Tax Profit Margin - 5YEAR AVRG.', 'Effective Tax Rate', 'Effective Tax Rate - 5YEAR AVRG.', 'Cash Conversion Cycle', 'Revenue per Employee', 'Net Income per Employee', 'Average Collection Period', 'Receivables Turnover', "Day's Inventory Turnover Ratio", 'Inventory Turnover', 'Inventory/Sales', 'Accounts Payble/Sales', 'Assets/Revenue', 'Net Working Capital Turnover', 'Fixed Assets Turnover', 'Total Assets Turnover', 'Revenue per $ Cash', 'Revenue per $ Plant', 'Revenue per $ Common Equity', 'Revenue per $ Capital Invested']

def getData(symbol):
    #url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22%20and%20%20xpath%3D'%2Fhtml%2Fbody%2Fform%2Ftable%5B5%5D%2Ftr%2Ftd%2Fcenter%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%5B3%5D%2Ftd%2Ftable%2Ftr'&diagnostics=true".replace('THE_STOCK_SYMBOL', symbol)
    #url = "http://query.yahooapis.com/v1/publicyql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22&diagnostics=true"
    #url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DCSCO%22%20and%20xpath%3D%22%2F%2Fbody%22&diagnostics=true"
    url = "http://www.advfn.com/p.php?pid=financials&btn=s_ok&mode=&symbol=THE_STOCK_SYMBOL&s_ok=OK".replace('THE_STOCK_SYMBOL', symbol)
    fd = urllib2.urlopen(url)
    x = fd.read()
    fd.close()
    z = ""
    y = x.split("\n")
    for line in y:
        z = z + line.strip() + " "
    return z

def getData_old(symbol):
    #url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22%20and%20%20xpath%3D'%2Fhtml%2Fbody%2Fform%2Ftable%5B5%5D%2Ftr%2Ftd%2Fcenter%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%5B3%5D%2Ftd%2Ftable%2Ftr'&diagnostics=true".replace('THE_STOCK_SYMBOL', symbol)
    #url = "http://query.yahooapis.com/v1/publicyql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22&diagnostics=true"
    #url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DCSCO%22%20and%20xpath%3D%22%2F%2Fbody%22&diagnostics=true"
    url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22&diagnostics=true".replace('THE_STOCK_SYMBOL', symbol)
    fd = urllib2.urlopen(url)
    x = fd.read()
    fd.close()
    z = ""
    y = x.split("\n")
    for line in y:
        z = z + line.strip() + " "
    return z

def getConnection(symbol):
    url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL%22&diagnostics=true".replace('THE_STOCK_SYMBOL', symbol)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection('query.yahooapis.com')
    conn.request("POST", "/v1/public/yql", 'q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.advfn.com%2Fp.php%3Fpid%3Dfinancials%26symbol%3DTHE_STOCK_SYMBOL'.replace('THE_STOCK_SYMBOL', symbol), headers)
    return conn
    #return json.loads(conn.getresponse().read())


def getXmlDocument(xmlText):
    return BeautifulSoup(xmlText)

def getXmlDocument_old(xmlText):
    theXml = StringIO.StringIO(xmlText)
    xmlDocument = lxml.etree.parse(theXml)
    return xmlDocument

def getField(xmlDocument, fieldName):
    return xmlDocument.find(text=fieldName)

def getField_old(xmlDocument, xpathString):
    return xmlDocument.xpath(xpathString)

def getFieldText(xmlDocument, xpathString):
    return getField(xmlDocument, xpathString)[0]

def getFinDataField(xmlDocument, dataFieldName):
    #print "DD" + dataFieldName
    #import pdb
    #pdb.set_trace()
    return {dataFieldName: getField(xmlDocument, dataFieldName).parent.parent.contents[1].text}

def getFinData(xmlDocument, dataFieldName):
    # try an exact match first
    #x = xmlDocument.xpath('/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[p="%s"]/../td[2]/p/text()' % (dataFieldName,))
    #dataFieldName = escape(dataFieldName)
    #print dataFieldName
    if dataFieldName == "COMPANYNAME":
        cname = xmlDocument.h1.text
        if len(cname) == 0:
            theName = "ERROR LOOKING UP COMPANY NAME"
        else:
            theName = cname
        return {"COMPANYNAME": theName}
    elif dataFieldName == "LATESTPRICE":
        try:
            #thePrice = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[2]/td/p[1]')
            #import pdb
            #pdb.set_trace()
            thePrice = xmlDocument.find(text="Price").parent.parent.parent.parent.findAll("td")[8].text
            #print "HHHHHHHHHH" + str(thePrice[0].text.strip())
            thePrice = str(thePrice.replace("&nbsp;", ""))
        except:
            thePrice = "0"
        return {"LATESTPRICE": thePrice}
    elif dataFieldName == "Beta":
        try:
            #theBeta = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            theBeta = xmlDocument.find(text="Beta").parent.parent.parent.parent.findAll("td")[26].text
            #print "HHHHHHHHHH" + str(theBeta[2].text.strip())
            theBeta = str(theBeta.replace("&nbsp;", ""))
        except:
            theBeta = "0"
        return {"Beta": theBeta}        
    elif dataFieldName == "52weekLow":
        try:
            #theRange = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            #import pdb
            #pdb.set_trace()
            theRange = xmlDocument.find(text="52-Wks-Range").parent.parent.parent.parent.findAll("td")[31].text
            #print "HHHHHHHHHH" + str(theRange[7].text.strip())
            theRange = str(theRange.strip())
            theRange = theRange.split("-")[1].strip().replace("&nbsp;", "")
            #print "HHHHHHHHHH" + theRange
        except:
            theRange = "0"
        return {"52weekLow": theRange}
        pass
    elif dataFieldName == "52weekHigh":
        try:
            #theRange = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            theRange = xmlDocument.find(text="52-Wks-Range").parent.parent.parent.parent.findAll("td")[31].text
            #print "HHHHHHHHHH" + str(theRange[7].text.strip())
            theRange = str(theRange.strip())
            theRange = theRange.split("-")[0].strip().replace("&nbsp;", "")
            #print "HHHHHHHHHH" + theRange
        except:
            theRange = "0"
        return {"52weekHigh": theRange}
        pass
    #x = xmlDocument.xpath('//td[p="%s"]/../td[2]/p/text()' % (dataFieldName,))
    x = getFinDataField(xmlDocument, dataFieldName)
    if len(x) > 1:
        #print "Incorrect number of matches found for field %s!!" % (dataFieldName,)
        pass
    #return {dataFieldName: x}
    return x
    # take only partial name to avoid whitespace issue
    #partialDataFieldName = dataFieldName[:16]
    #x = xmlDocument.xpath('/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[starts-with(p, "%s")]/../td[2]/p/text()' % (partialDataFieldName,))
    #x = xmlDocument.xpath('//td[starts-with(p, "%s")]/../td[2]/p/text()' % (partialDataFieldName,))
    #/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[starts-with(p, '
    #if len(x) > 1:
    #    print "Incorrect number of matches found for field %s!!" % (partialDataFieldName,)
    #return {dataFieldName: x[0]}

def getFinData_old(xmlDocument, dataFieldName):
    # try an exact match first
    #x = xmlDocument.xpath('/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[p="%s"]/../td[2]/p/text()' % (dataFieldName,))
    #dataFieldName = escape(dataFieldName)
    if dataFieldName == "COMPANYNAME":
        cname = xmlDocument.xpath("//h1/text()")
        if len(cname) == 0:
            theName = "ERROR LOOKING UP COMPANY NAME"
        else:
            theName = cname[0]
        return {"COMPANYNAME": theName}
    elif dataFieldName == "LATESTPRICE":
        try:
            thePrice = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[2]/td/p[1]')
            #print "HHHHHHHHHH" + str(thePrice[0].text.strip())
            thePrice = str(thePrice[0].text.strip())
        except:
            thePrice = "0"
        return {"LATESTPRICE": thePrice}
    elif dataFieldName == "Beta":
        try:
            theBeta = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            #print "HHHHHHHHHH" + str(theBeta[2].text.strip())
            theBeta = str(theBeta[2].text.strip())
        except:
            theBeta = "0"
        return {"Beta": theBeta}        
    elif dataFieldName == "52weekLow":
        try:
            theRange = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            #print "HHHHHHHHHH" + str(theRange[7].text.strip())
            theRange = str(theRange[7].text.strip())
            theRange = theRange.split("-")[1].strip()
            #print "HHHHHHHHHH" + theRange
        except:
            theRange = "0"
        return {"52weekLow": theRange}
        pass
    elif dataFieldName == "52weekHigh":
        try:
            theRange = xmlDocument.xpath('//table/tr/td/p[span="Price"]/../../../tr[4]/td/p[1]')
            #print "HHHHHHHHHH" + str(theRange[7].text.strip())
            theRange = str(theRange[7].text.strip())
            theRange = theRange.split("-")[0].strip()
            #print "HHHHHHHHHH" + theRange
        except:
            theRange = "0"
        return {"52weekHigh": theRange}
        pass
    x = xmlDocument.xpath('//td[p="%s"]/../td[2]/p/text()' % (dataFieldName,))
    if len(x) > 1:
        #print "Incorrect number of matches found for field %s!!" % (dataFieldName,)
        pass
    return {dataFieldName: x[0]}
    # take only partial name to avoid whitespace issue
    #partialDataFieldName = dataFieldName[:16]
    #x = xmlDocument.xpath('/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[starts-with(p, "%s")]/../td[2]/p/text()' % (partialDataFieldName,))
    #x = xmlDocument.xpath('//td[starts-with(p, "%s")]/../td[2]/p/text()' % (partialDataFieldName,))
    #/query/results/body/form/table/tr/td/center/table/tr/td/table/tr/td/table/tr/td[starts-with(p, '
    #if len(x) > 1:
    #    print "Incorrect number of matches found for field %s!!" % (partialDataFieldName,)
    #return {dataFieldName: x[0]}


def getAllFieldPairs(symbol):
    x = getData(symbol)
    xmlDocument = getXmlDocument(x)
    return [getFinData(xmlDocument, i) for i in field_list_1] + [getFinData(xmlDocument, i) for i in field_list_2] + [getFinData(xmlDocument, i) for i in field_list_3] + [getFinData(xmlDocument, 'COMPANYNAME')] + [getFinData(xmlDocument, 'LATESTPRICE')] + [getFinData(xmlDocument, 'Beta')] + [getFinData(xmlDocument, '52weekLow')] + [getFinData(xmlDocument, '52weekHigh')]

def getAllFields(symbol):
    try:
        x = getAllFieldPairs(symbol)
        y = {}
        for i in x:
            y.update(i)
        y['symbol'] = symbol
        #y.update(fetchHotness(y['COMPANYNAME']))
        return y
    except Exception:
        print >> sys.stderr, "Symbol [%s], [%s], [%s]" % (symbol, sys.exc_info()[0], sys.exc_info()[1])
        import pdb
        #pdb.set_trace()
        return None

sorted_field_list = ['symbol', 'COMPANYNAME', 'LATESTPRICE', 'Beta', '52weekLow', '52weekHigh', '5-Y Average P/E Ratio', '5-Y High P/E Ratio', '5-Y Low P/E Ratio', 'Accounts Payble/Sales', "Altman's Z-Score Ratio", 'Assets Productivity', 'Assets Turnover', 'Assets/Revenue', 'Average Collection Period', 'Book Value pS - LTM', 'Book-Value pS', 'Capital Invested Productivity', 'Capital Invested pS', 'Cash Conversion Cycle', 'Cash Flow pS', 'Cash Flow pS - LTM', 'Cash pS', 'Cash pS - LTM', 'Cash-Flow pS', 'Current 12 Month Normalized P/E Ratio - LTM', 'Current Liabilities pS', 'Current P/E Ratio - LTM', 'Current P/E Ratio as % of 5-Y Average P/E', 'Current Ratio', "Day's Inventory Turnover Ratio", 'Debt Ratio', 'Dividend Payout Ratio', 'Dividend Yield', 'Dividend pS (DPS)', 'Domestic Sales', 'EBIT Margin - LTM', 'EBITDA Margin', 'EBITDA Margin - LTM', 'Earnings pS (EPS)', 'Effective Tax Rate', 'Effective Tax Rate - 5YEAR AVRG.', 'Enterprise Value (EV)/EBITDA', 'Enterprise Value (EV)/Free Cash Flow', 'Equity Productivity', 'Financial Leverage Ratio (Assets/Equity)', 'Fixed Assets Turnover', 'Float', 'Float as % of Shares Outstanding', 'Foreign Sales', 'Free Cash Flow Margin', 'Free Cash Flow Margin 5YEAR AVG', 'Free Cash Flow pS', 'Free Cash Flow pS - LTM', 'Free Cash-Flow pS', 'Gross Profit Margin', 'Gross Profit Margin - 5YEAR AVRG.', 'Interest Cover', 'Interest/Capital Invested', 'Inventory Turnover', 'Inventory/Sales', 'LT Debt pS', 'LT Debt/Capital Invested', 'LT Debt/Equity', 'LT Debt/Total Capital', 'LT Debt/Total Liabilities', 'Latest Shares Outstanding', 'Leverage Ratio (Assets/Equity)', 'Liquidity Ratio (Cash)', 'Market Capitalisation', 'Net Income per Employee', 'Net Profit Margin', 'Net Profit Margin - 5YEAR AVRG.', 'Net Working Capital Ratio', 'Net Working Capital Turnover', 'P/E Ratio (1 month ago) - LTM', 'P/E Ratio (26 weeks ago) - LTM', 'P/E Ratio (52 weeks ago) - LTM', 'P/E as % of Industry Group', 'P/E as % of Sector Segment', 'PE Ratio - LTM', 'PQ Ratio', 'Pre-Tax Profit Margin', 'Pre-Tax Profit Margin - 5YEAR AVRG.', 'Price/Book Ratio', 'Price/Book Ratio - LTM', 'Price/Cash Flow', 'Price/Cash Flow Ratio', 'Price/Free Cash Flow', 'Price/Free Cash Flow Ratio - LTM', 'Price/Sales Ratio', 'Price/Tangible Book Ratio', 'Price/Tangible Book Ratio - LTM', 'Quick Ratio (Acid Test)', 'R&D Expense as % of Revenue - 5YEAR AVRG.', 'Receivables Turnover', 'Research & Devlopment (R&D) as % of Revenue', 'Return on Assets (ROA)', 'Return on Assets (ROA) - 5YEAR AVRG.', 'Return on Capital Invested (ROCI)', 'Return on Capital Invested (ROCI) - 5YEAR AVRG.', 'Return on Equity (ROE)', 'Return on Equity (ROE) - 5YEAR AVRG.', 'Revenue per $ Capital Invested', 'Revenue per $ Cash', 'Revenue per $ Common Equity', 'Revenue per $ Plant', 'Revenue per Employee', 'SG&A Expense as % of Revenue - 5YEAR AVRG.', 'Tangible Book Value pS - LTM', 'Tangible Book-Value pS', "Tobin's Q Ratio", 'Total Assets Turnover', 'Total Debt/Equity (Gearing Ratio)', 'Working Capital pS', 'Working Capital/Equity']

def processSymbols_old(symbolList=sys.argv[1:]):
    data = []
    return filter(None, map(getAllFields, symbolList))
    for theSymbol in symbolList:
        try:
            theData = getAllFields(theSymbol)
            data.append(theData)
        except:
            print >> sys.stderr, "Failed trying to get data for %s" % (theSymbol,)
    return data

def processSymbols(symbolList=sys.argv[1:]):
    pool = multiprocessing.Pool(processes=50)
    return filter(None, pool.map(getAllFields, symbolList))
    #return filter(None, map(getAllFields, symbolList))

#from pyGTrends import pyGTrends
#connector = pyGTrends('mohanraotekale','tekalemohan')

def fetchHotness(companyName, numPeriods=5):
    connector.download_report((companyName))
    lines = connector.csv().split('\n')
    skipCount = -len(lines)/numPeriods
    periods = {}
    count = 0
    for i in range(len(lines)-1, 1, skipCount):
        periods['t-minus-%03d' % (count,)] = lines[i].split(",")[1].strip()
        count += 1
    return periods

if __name__ == '__main__':
    data = processSymbols(sys.argv[1:])
    csvutil.writeCSVContentsFromDictionaries(data, sorted_field_list)
    #getData(t)

