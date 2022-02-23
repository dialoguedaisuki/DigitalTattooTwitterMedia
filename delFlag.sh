#!/bin/sh
IFS='\n'
echo "envName=" $1
echo "word=" $2
echo "db_envName=" $3
mkdir -p ~/log/$1
python3 ~/DigitalTattooTwitterMedia/delFlagInsert.py $1 $3 2>&1 | tee ~/log/$1/`date "+%Y%m%d_%H%M%S"`.insDelFlag.log