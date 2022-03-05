#!/bin/sh
IFS='\n'
echo "plusPath=" $1
echo "db_envName=" $2
echo "envName=" $3
mkdir -p ~/log/$3
python3 ~/DigitalTattooTwitterMedia/identifiesImageInsert.py $1 $2 2>&1 | tee ~/log/$3/`date "+%Y%m%d_%H%M%S"`.score.log