import StringIO, sys, os, urllib2, httplib, multiprocessing, re
#from xml.sax.saxutils import escape
import csvutil
from BeautifulSoup import BeautifulSoup

balanceSheetFieldList = ['Cash & Equivalents', 'Receivables', 'Notes Receivable', 'Inventories', 'Other Current Assets', 'Total Current Assets', 'Net Property & Equipment', 'Investments & Advances', 'Other Non-Current Assets', 'Deferred Charges', 'Intangibles', 'Deposits & Other Assets', 'Total Assets', 'Notes Payable', 'Accounts Payable', 'Current Portion Long-Term Debt', 'Current Portion Capital Leases', 'Accrued Expenses', 'Income Taxes Payable', 'Other Current Liabilities', 'Total Current Liabilities', 'Mortgages', 'Deferred Taxes/Income', 'Convertible Debt', 'Long-Term Debt', 'Non-Current Capital Leases', 'Other Non-Current Liabilities', 'Minority Interest (Liabilities)', 'Total Liabilities', 'Preferred Stock', 'Common Stock (Par)', 'Capital Surplus', 'Retained Earnings', 'Other Equity', 'Treasury Stock', "Total Shareholder's Equity", "Total Liabilities & Shareholder's Equity", 'Total Common Equity', 'Shares Outstanding', 'Book Value Per Share']

incomeStatementFieldList = ['Sales', 'Cost Of Goods', 'Gross Profit', 'Selling & Adminstrative & Depr. & Amort Expenses', 'Income After Depreciation & Amortization', 'Non-Operating Income', 'Interest Expense', 'Pretax Income', 'Income Taxes', 'Minority Interest', 'Investment Gains/Losses', 'Other Income/Charges', 'Income From Cont. Operations', 'Extras & Discontinued Operations', 'Net Income', 'Income Before Depreciation & Amortization', 'Depreciation & Amortization (Cash Flow)', 'Income After Depreciation & Amortization', 'Average Shares', 'Diluted EPS Before Non-Recurring Items', 'Diluted Net EPS']

cashFlowStatementFieldList = ['Net Income (Loss)', 'Depreciation/', 'Net Change from Assets/Liabilities', 'Net Cash from Discontinued Operations', 'Other Operating Activities', 'Net Cash From Operating Activities', 'Property & Equipment', 'Acquisition/ Disposition of Subsidiaries', 'Investments', 'Other Investing Activities', 'Net Cash from Investing Activities', 'Issuance (Repurchase) of Capital Stock', 'Issuance (Repayment) of Debt', 'Increase (Decrease) Short-Term Debt', 'Payment of Dividends', 'Other Financing Activities', 'Net Cash from Financing Activities', 'Effect of Exchange', 'Net Change In Cash & Equivalents', 'Cash at Beginning of Period', 'Cash at End of Period', 'Diluted Net EPS']


def getStatementField(xmlDocument, fieldName):
    r = re.compile('^' + re.escape(fieldName), re.I)
    return xmlDocument.findAll(text=fieldName)

def getBalanceSheet(symbol):
    pass

def getIncomeStatement(symbol):
    pass

def getCashFlowStatement(symbol):
    pass

if __name__ == '__main__':
    pass
