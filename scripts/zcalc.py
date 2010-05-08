import sys, json

#T1 = (Current Assets-Current Liabilities) / Total Assets
#T2 = Retained Earnings / Total Assets
#T3 = Earnings Before Interest and Taxes / Total Assets
#T4 = Book Value of Equity / Total Liabilities
#T5 = Sales/ Total Assets

def getAllTs(balanceSheet, cashFlow, income):
    numShares = float(balanceSheet['Total Common Shares Outstanding'])
    closePrice = float(balanceSheet['Historical-Quote'].split('\n')[1].split(',')[4])
    marketCap = numShares * closePrice
    t1 = (float(balanceSheet['Total Current Assets']) - float(balanceSheet['Total Current Liabilities'])) / float(balanceSheet['Total Assets'])
    t2 = float(balanceSheet['Retained Earnings (Accumulated Deficit)']) / float(balanceSheet['Total Assets'])
    t3 = float(income['Operating Income']) / float(balanceSheet['Total Assets'])
    t4 = marketCap / float(balanceSheet['Total Liabilities'])
    t5 = float(income['Total Revenue']) / float(balanceSheet['Total Assets'])
    #print balanceSheet['Historical-Quote']
    return t1, t2, t3, t4, t5

def getZScore(t1, t2, t3, t4, t5):
    #Z = 1.2T1 + 1.4T2 + 3.3T3 + 0.6T4 + 0.999T5
    z = 1.2*t1 + 1.4*t2 + 3.3*t3 + 0.6*t4 + 0.999*t5
    return z

def getDataForSymbol(symbol, periodType):
    x = urllib2.urlopen("http://localhost:8080/fundamental/fundie/CSCO/Qtr")
    xxx = x.read()
    yyy = json.loads(xxx, strict=False)
    len(yyy)
    yyy = yyy['data']
    apply(getZScore, getAllTs(yyy[0][1], yyy[1][1], yyy[2][1]))
