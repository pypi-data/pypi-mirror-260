#!/bin/bash

PROCESS_TYPE=$1

litenchat=`which litenchat.py`
if [ -z "${litenchat}" ]; then
    echo "litenchat.py not found"
    exit 1
fi
echo "Starting litenchat = ${litenchat} with process type ${PROCESS_TYPE}"

if [ "$PROCESS_TYPE" == "daemon" ];
then
    nohup -- python3 ${litenchat} >& /dev/null &
else
    python3 ${litenchat}
fi
