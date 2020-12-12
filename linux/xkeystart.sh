#!/bin/bash
# >/dev/null 2>&1

if [ -f /usr/local/bin/xkeysnail ];then
	xkeyfullpath="/usr/local/bin/xkeysnail"
elif [ -f /usr/bin/xkeysnail ];then
	xkeyfullpath="/usr/bin/xkeysnail"
else
	xkeyfullpath=`which xkeysnail`
fi

"$xkeyfullpath" --quiet --watch "$1" &

inotifywait -m -e close_write,moved_to,create,modify /tmp/kinto/xkeysnail |

while read -r path; do
	/usr/bin/killall xkeysnail
	"$xkeyfullpath" --quiet --watch "$1" &
done