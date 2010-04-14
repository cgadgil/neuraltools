#!/bin/bash

svn log -v --xml http://172.21.52.55/svn/vsx/trunk> /tmp/svn.log
java -jar /home/cgadgil/downloads/statsvn-0.5.0/statsvn.jar -include "**/*.java;**/*xml;**/*.as;**/*.txt;**/*config;**/*properties;**/*.py;**/*.groovy;**/*.sql" -output-dir /var/www/svninfo/vsx/ /tmp/svn.log /home/cgadgil/mensa/svn/vsx/trunk/

