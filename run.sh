#!/bin/sh

DIRNAME=$(dirname $0)
cd $DIRNAME
INSTALL=$(pwd)

runfile=/tmp/run$$.txt

python3 $INSTALL/__init__.py | tee $runfile

cat $runfile | mail -s "Video Distribution" root

rm $runfile
