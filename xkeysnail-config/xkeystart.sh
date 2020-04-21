#!/bin/bash
# >/dev/null 2>&1
/usr/local/bin/xkeysnail --quiet --watch "$1" &
while true
	do inotifywait -e close_write,moved_to,create -q "$1"
		/usr/bin/killall xkeysnail
		/usr/local/bin/xkeysnail --quiet --watch "$1" &
done