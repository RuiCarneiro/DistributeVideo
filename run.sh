#!/bin/sh

DIRNAME=$(dirname $0)
cd $DIRNAME
INSTALL=$(pwd)

runfile=/tmp/run$$.txt

echo "Distribution of video files" > $runfile
date >> $runfile
python3 $INSTALL/__init__.py | tee -a $runfile
echo End >> $runfile

cat $runfile | mail -s "Video Distribution" root

rm $runfile
