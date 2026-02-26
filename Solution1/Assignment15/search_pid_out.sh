#!/bin/bash

HOSTNAMES_FILE=$1
USER=$2
PROCESS=$3
OUTPUT=$4

for line in $(cat "$HOSTNAMES_FILE"); do
  ssh -o "StrictHostKeyChecking=no" "$line" "
  if pgrep -u \"$USER\" -x \"$PROCESS\" && [ -f /tmp/ppurld.out ]; then
    cat /tmp/ppurld.out | tr 'A-Za-z' 'N-ZA-Mn-za-m'
  fi
  " >> "$OUTPUT" || continue
done
website=$(sed -n '5p' "$OUTPUT")
wget -qO- "$website" | grep -oP '([^<]+)'

