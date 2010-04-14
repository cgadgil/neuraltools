#!/bin/env python

import sys

def findreplace(fileName, findString, replaceString):
    fd = file(fileName)
    d = fd.read()
    d = d.replace(findString, replaceString)
    fd.close()
    fd = file(fileName, "w")
    fd.write(d)
    fd.close()

if __name__ == "__main__":
    fileName, findString, replaceString = sys.argv[1:4]
    findreplace(fileName, findString, replaceString)

