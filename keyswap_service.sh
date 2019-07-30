#!/bin/bash

swapbehavior=$1
newparams=$2
noswapcmd=$3

if [[ "$swapbehavior" == "yes" ]]; then
	swapcmd="/bin/bash /home/`whoami`/.config/xactive.sh $2"

	cp ./system-config/keyswap.service ~/.config/systemd/user/keyswap.service
	sed -i "s/{username}/${whoami}/g" ~/.config/systemd/user/keyswap.service
	sed -i "s/ExecStart=/ExecStart=${swapcmd}/g" ~/.config/systemd/user/keyswap.service
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