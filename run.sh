#!/bin/bash

#Configuration here

EMAIL=1                 # Change to zero to disable. Requires working MTA
EMAIL_SUBJECT="Video files distribution"  #Keep between quotation marks
EMAIL_RECIPIENT=root    # Change to your e-mail address if needed.

#End of configuration


DIRNAME=$(dirname $0)
cd $DIRNAME
INSTALL=$(pwd)

runfile=/tmp/run$$.txt

date >> $runfile
python3 $INSTALL/__init__.py | tee -a $runfile

if [ $EMAIL = "1" ]; then
	cat $runfile | mail -s "$EMAIL_SUBJECT" $EMAIL_RECIPIENT
fi

rm $runfile
