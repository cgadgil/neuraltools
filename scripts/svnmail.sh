#!/bin/env bash

currentRev=`svn info|grep Revision|sed -e 's/Revision: //g'`
previousRev=`cat .previous-rev`
