#!/bin/bash

#PROCESS_NAME=$1
#USER_NAME=$2

PIDS=$(pgrep -u "$2" -x "$1")
if [ -n "$PIDS" ]; then
  exit 1
else
  exit 0
fi
