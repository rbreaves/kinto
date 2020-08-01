#!/bin/bash
# /usr/local/bin/logoff.sh
while true; do
  w | grep -E "$1.*$2" > /dev/null 2>&1 || (sudo systemctl stop xkeysnail && sudo pkill -f logoff)
  sleep 5
done