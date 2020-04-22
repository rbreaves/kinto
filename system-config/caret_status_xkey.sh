#!/bin/bash

# silent_background() {
#     { 2>&3 "$@"& } 3>&2 2>/dev/null
#     disown &>/dev/null 
# }

mkdir -p /tmp/kinto
echo "0" > /tmp/kinto/caret
# background process that will check
# caret status and apply keymap
lastcheck=0
ww=0
while (true);do
	sleep 0.2
	check=$(cat /tmp/kinto/caret)
	if [ "${check}" == "ff ww 1" ] && [ "${lastcheck}" != 1 ]; then
		echo "firefox wordwise"
		# echo "$check"
		# Sets original config
		perl -pi -e "s/(# )(.*)(# Beginning of Line)/\$2\$3/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(# )(.*)(# End of Line)/\$2\$3/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(\w.*)(# Firefox-nw)/# \$1\$2/g" /tmp/kinto/kinto.py
		lastcheck=1
		ww=1
	elif [ "${check}" == "ff nw" ] && [ "${lastcheck}" != 2 ]; then
		echo "firefox no wordwise"
		# echo "$check"
		# Sets new config
		perl -pi -e "s/(# )(.*)(# Firefox-nw)/\$2\$3/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(\w.*)(# Beginning of Line)/# \$1\$2/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(\w.*)(# End of Line)/# \$1\$2/g" /tmp/kinto/kinto.py
		lastcheck=2
		ww=0
	elif [ "${check}" == "chrome ww 1" ] && [ "${lastcheck}" != 3 ]; then
		echo "chrome wordwise"
		# echo "$check"
		# Sets original config
		perl -pi -e "s/(\w.*)(# Beginning of Line)/\$1\$2/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(\w.*)(# End of Line)/\$1\$2/g" /tmp/kinto/kinto.py
		lastcheck=3
		ww=1
	elif [ "${check}" == "chrome nw" ] && [ "${lastcheck}" != 4 ]; then
		echo "chrome no wordwise"
		# echo "$check"
		# Sets new config
		perl -pi -e "s/(# )(.*)(# Beginning of Line)/\$2\$3/g" /tmp/kinto/kinto.py
		perl -pi -e "s/(# )(.*)(# End of Line)/\$2\$3/g" /tmp/kinto/kinto.py
		lastcheck=4
		ww=0
	elif [ "${check}" == "reset" ] && [ "${lastcheck}" != 5 ]; then
		echo "reset"
		# cp /home/{username}/.config/kinto/kinto.py /tmp/kinto/kinto.py
		lastcheck=5
	fi
	# echo "outside loop $check"
done &

lastapp="None"
reset=false
IBUSADD=$(cat ~/.config/ibus/bus/`ls ~/.config/ibus/bus -1rt | tail -n1` | awk -F'IBUS_ADDRESS=' '{print $2}' | xargs)
dbus-monitor --address $IBUSADD "path='/org/freedesktop/IBus/Panel',interface='org.freedesktop.IBus.Panel',member='FocusOut'" 2> /dev/null | grep --line-buffered -o -P '(?<=object path \"/org/freedesktop/IBus/InputContext_).*(?=[\"])' |
while read ln
do
	appname=$(xprop -id `xprop -root | grep "_NET_ACTIVE_WINDOW(WINDOW)" | awk '{print $5}'` | grep "WM_CLASS(STRING)" | awk '{print substr($4,2,length($4)-2)}')
	# Enable wordwise
	if (( $ln == 1 )); then
		if [ "${appname}" == "Firefox" ] && [ "${laststatus}" != "1" ]; then
			printf 'ff ww %s\n' "$ln" > /tmp/kinto/caret
			reset=false
		elif [ "${appname}" == "Chromium" ] || [ "${appname}" == "Chromium-browser" ] || [ "${appname}" == "Google-chrome" ] || [ "${appname}" == "Epiphany" ] && [ "${laststatus}" != "1" ]; then
			printf 'chrome ww %s\n' "$ln" > /tmp/kinto/caret
			reset=false
		elif ! [ "${appname}" == "Firefox" ] || [ "${appname}" == "Chromium" ] || [ "${appname}" == "Chromium-browser" ] || [ "${appname}" == "Google-chrome" ] || [ "${appname}" == "Epiphany" ] && [ "${reset}" == false ]; then
			echo "reset" > /tmp/kinto/caret
			reset=true
		fi

		lastapp="$appname"
		laststatus="$ln"
	#printf '%s\n' "$ln" > /tmp/kinto/caret
	# disable wordwise
	else
		if [ "${appname}" == "Firefox" ] && [ "${laststatus}" == "1" ]; then
			printf 'ff nw\n' > /tmp/kinto/caret
			reset=false
		elif [ "${appname}" == "Chromium" ] || [ "${appname}" == "Chromium-browser" ] || [ "${appname}" == "Google-chrome" ] || [ "${appname}" == "Epiphany" ] && [ "${laststatus}" == "1" ]; then
			printf 'chrome nw\n' > /tmp/kinto/caret
			reset=false
		elif ! [ "${appname}" == "Firefox" ] || [ "${appname}" == "Chromium" ] || [ "${appname}" == "Chromium-browser" ] || [ "${appname}" == "Google-chrome" ] || [ "${appname}" == "Epiphany" ] && [ "${reset}" == false ]; then
			echo "reset" > /tmp/kinto/caret
			reset=true
		fi
		lastapp="$appname"
		laststatus="$ln"
	fi
done
