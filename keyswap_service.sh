#!/bin/bash

swapbehavior=$1
noswapcmd=$2

systemtype=$3
internalid=$4
usbid=$5
chromeswap=$6

if [[ "$swapbehavior" == "1" ]]; then
	swapcmd="\/bin\/bash\ \/home\/`whoami`\/.config\/xactive.sh\ ${systemtype}\ ${internalid}\ ${usbid}\ ${chromeswap}"
	mkdir -p ~/.config/systemd/user
	mkdir -p ~/.config/autostart
	cp ./system-config/keyswap.service ~/.config/systemd/user/keyswap.service
	cp ./system-config/keyswap.sh ~/.config/autostart/keyswap.sh
	cp ./system-config/xactive.sh ~/.config/xactive.sh
	sed -i "s/{username}/`whoami`/g" ~/.config/systemd/user/keyswap.service
	sed -i "s/ExecStart=/ExecStart=${swapcmd}/g" ~/.config/systemd/user/keyswap.service
	systemctl --user enable keyswap
	systemctl --user start keyswap
else
	#/usr/bin/setxkbmap
	#/usr/bin/xkbcomp
	#echo $XDG_SESSION_TYPE
	if [ ! -f "~/.Xsession" ]; then
		echo "$noswapcmd" > ~/.Xsession
	fi
	grep "xkb" ~/.Xsession 1>/dev/null
	if [ $? -eq 1 ]; then
		echo "$noswapcmd" >> ~/.Xsession
	fi
fi