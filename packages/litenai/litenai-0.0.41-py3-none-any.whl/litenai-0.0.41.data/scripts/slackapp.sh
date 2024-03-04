#!/bin/bash
PROCESS_TYPE=$1
slackapp=`which slackapp.py`
if [ -z "${slackapp}" ]; then
    echo "slackapp.py not found"
    exit 1
fi
echo "Starting slack app ${slackapp} with process type ${PROCESS_TYPE}  ..."

if [ "$PROCESS_TYPE" == "daemon" ];
then
    nohup -- python3 ${slackapp} >& /dev/null &
else
    python3 ${slackapp}
fi
