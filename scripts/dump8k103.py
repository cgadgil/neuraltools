#!/bin/env python

import time, urllib2, sys

#for i in `(wget -O - http://www.sec.gov/news/digest/2010/dig032210-8k.txt 2>/dev/null|grep "1\.03"|while read line; do echo $line|sed -e s/ [A-Z]{2} //g|sed -e s/[0-9.]//g|sed -es/,.*//g|sed -e s/ [A-Z][A-Z] //g|sed -e s/ /+/g|grep -v Receiver; done)`; do blah=`echo "http://www.bing.com/search?q=BLAHBLAH+NYSE:&format=rss"|sed -e "s/BLAHBLAH/$i/g"`; echo $blah; python t.py $blah 5 8k103 sec8k103; done

def getDataForDate(timeStampSeconds=time.time()):
    found = []
    secUrl = time.strftime('http://www.sec.gov/news/digest/2010/dig%m%d%y-8k.txt', time.localtime(timeStampSeconds))
    fd = urllib2.urlopen(secUrl)
    for line in fd:
        if line.count('1.03') != 0:
            found.append(line.strip())
    fd.close()
    return found[1:]

def getDataForPastDays(numDays=30):
    found = []
    for i in range(numDays):
        timeStampSeconds = time.time() - i*86400
        try:
            found = found + getDataForDate(timeStampSeconds)
        except:
            print >>sys.stderr, i
    return found

if __name__ == '__main__':
    numDays = int(sys.argv[1])
    dataLines = getDataForPastDays(numDays)
    print "\n".join(dataLines)

