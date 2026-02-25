#!/bin/bash

REMOTE_LOGIN=$1

ssh -o "StrictHostKeyChecking=no" $REMOTE_LOGIN "cat /proc/loadavg" | cut -f 2 d " " | awk '{print $1 * 100}'