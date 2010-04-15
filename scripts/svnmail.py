#!/bin/env python

#svn diff -c 3|python /tmp/ud2html.py -k -l 600|~/src/scripts/htmlemail.sh |sendmail cgadgil@cisco.com

import os, subprocess

tmpl = """From: %s
To: %s
Subject: [SVN checkin] %s
MIME-Version: 1.0
Content-Type: text/html
Content-Disposition: inline
"""

def failedstate(*args):
    if len(args) == 1:
        fd = file(".failed-state", "w")
        fd.write(str(args[0]))
        fd.close()
    elif len(args) == 0:
        fd = file(".failed-state")
        x = fd.read()
        fd.close()
        return int(x.strip())
    return -1

def getProcessOutputLines(cmdline):
    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, shell=True)
    return p.stdout.readlines()

def getCurrentVersion():
    p = subprocess.Popen("svn info http://172.21.52.55/svn|grep Revision|sed -e 's/Revision: //g'", stdout=subprocess.PIPE, shell=True)
    return int(p.communicate()[0].strip())

def getPreviousVersion():
    fd = file(".previous-rev")
    vnum = fd.read().strip()
    fd.close()
    return int(vnum)

def updatePreviousVersion(vNum):
    fd = file(".previous-rev", "w")
    print >> fd, str(vNum)
    fd.close()

def getSvnLogLines(vNum):
    return getProcessOutputLines("svn log -r %s http://172.21.52.55/svn" % (str(vNum),))

# output=`dmesg | grep hda`
# ==>
# p1 = Popen(["dmesg"], stdout=PIPE)
# p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
# output = p2.communicate()[0]

def mailDiff():
    oldRev = getPreviousVersion()
    newRev = getCurrentVersion()
    print oldRev, newRev
    if newRev > oldRev:
        newRev = oldRev + 1
        subject = getSvnLogLines(newRev)[3].strip()
        fromAddr = getSvnLogLines(newRev)[1].split()[2] + "@cisco.com"
        toAddr = "vsx-checkins@cisco.com"
        malida = "".join(getProcessOutputLines("svn diff -x -w -r %s:%s ..|python ~/src/scripts/ud2html.py -k -l 600" % (oldRev, newRev)))
        #print malida
        #x = "svn log -r %s; svn diff -x -w -r %s:%s|python ~/src/scripts/ud2html.py -k -l 600)"
        p = subprocess.Popen("sendmail %s" % (toAddr,), shell=True, stdin=subprocess.PIPE)
        print 'p = subprocess.Popen("sendmail %s" % (toAddr,), shell=True, stdin=subprocess.PIPE)'
        #print tmpl % (fromAddr, toAddr, subject)
        p.stdin.write(tmpl % (fromAddr, toAddr, subject))
        p.stdin.write(malida)
        p.stdin.close()
        updatePreviousVersion(newRev)
        print "/home/cgadgil/src/resolvebug.sh %s %s" % (str(oldRev), str(newRev))
        os.system("/home/cgadgil/src/resolvebug.sh %s %s" % (str(oldRev), str(newRev)))
        doBuild()
    else:
        print "No updates"

def doBuild():
    x = os.system("mvn clean install > /tmp/bld.log 2>&1")
    if x:
        os.system("tail -500 /tmp/bld.log | mail -s 'build failed' vsx-checkins@cisco.com")
        failedstate(1)
    else:
        if failedstate() == 1:
            os.system("echo Thanks | mail -s 'build fixed' vsx-checkins@cisco.com")
        failedstate(0)
    os.system("bash ~/src/scripts/svninfo.sh")

if __name__ == "__main__":
    mailDiff()



