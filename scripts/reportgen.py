#!/bin/env python

import csv,sys,os, cStringIO

from mako.template import Template

theTemplateString = """
<html>
<head>MAGI CAPITAL INVESTMENT CLUB REPORT</head>
<body>
% for line in lines:
<%
SYMBOL = line.split()[0].strip()
RECOMMENDATION = line.split()[1].strip()
%>
<h3>Data on ${SYMBOL}, recommendation ${RECOMMENDATION}</h3>
<table>
<tr>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=ps_ratio&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a></p>
</td>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=peg_ratio&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a></p>
</td>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=price_to_book_value&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a> </p>
</td>
</tr>
<tr>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=revenue_growth&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a> </p>
</td>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=price&amp;start_date=2009-12-14&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a> by <a href="http://ycharts.com">YCharts</a></p>
</td>
<td>
<iframe src="http://ycharts.com/companies/${SYMBOL}/embediframe?partner=basic_iframe&amp;calc=return_on_equity&amp;end_date=2011-12-14&amp;format=real" width="400" height="290" scrolling="no" frameborder="0" marginwidth="0" marginheight="0"></iframe><p><a href="http://ycharts.com/companies/${SYMBOL}">${SYMBOL} Stock Chart</a> </p>
</td>
</tr>
</table>
% endfor

% for line in lines:
<%
SYMBOL = line.split()[0].strip()
RECOMMENDATION = line.split()[1].strip()
%>
<h3>Data on ${SYMBOL}, recommendation ${RECOMMENDATION}</h3>
<table>
<tr>
<td>
<a href="http://www.advfn.com/p.php?pid=financials&symbol=${SYMBOL}">${SYMBOL}</a>
</td>
</tr>
</table>
% endfor

</body>
</html>
"""

def genReport(lines):
    theTemplate = Template(theTemplateString)
    return theTemplate.render(lines=lines)

if __name__ == '__main__':
    lines = sys.stdin.readlines()
    print genReport(lines=lines)

