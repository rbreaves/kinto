#!/bin/bash


if [ $# -eq 0 ]; then
	echo "Install Kinto - xkeysnail (udev)"
	echo "  1) Windows & Mac (HID driver)"
	echo "  2) Mac Only & VMs on Macbooks"
	echo "  3) Chromebook"

	read n

	set "$n"
fi

if [[ $1 == "1" || $1 == "2" || $1 == "3" || $1 == "winmac" || $1 == "mac" || $1 == "chromebook" ]]; then
	# echo "Transferring files..."
	mkdir -p ~/.config/kinto
	
	# KDE xhost fix
	mkdir -p ~/.kde/Autostart
	echo -e '#!/bin/sh\rxhost +SI:localuser:root' > ~/.kde/Autostart/kintohost.sh
	chmod +x ~/.kde/Autostart/kintohost.sh

	cp ./xkeysnail-config/kinto.py ./xkeysnail-config/kinto.py.new
	cp ./xkeysnail-config/prexk.sh ~/.config/kinto/prexk.sh
	cp ./xkeysnail-config/xkeysnail.service ./xkeysnail-config/xkeysnail.service.new
	sed -i "s/{username}/`whoami`/g" ./xkeysnail-config/xkeysnail.service.new
	sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ./xkeysnail-config/xkeysnail.service.new
else
	echo "Expected argument was not provided"
fi

if [[ $1 == "1" || $1 == "winmac" ]]; then
	echo '1' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd;echo 'options hid_apple swap_opt_cmd=1' | sudo tee -a /etc/modprobe.d/hid_apple.conf;sudo update-initramfs -u -k all
	perl -pi -e "s/(# )(.*)(# WinMac)/\$2\$3/g" ./xkeysnail-config/kinto.py.new
elif [[ $1 == "2" || $1 == "mac" ]]; then
	perl -pi -e "s/(# )(.*)(# Mac)/\$2\$3/g" ./xkeysnail-config/kinto.py.new
elif [[ $1 == "3" || $1 == "chromebook" ]]; then
	perl -pi -e "s/(# )(.*)(# Chromebook)/\$2\$3/g" ./xkeysnail-config/kinto.py.new
	perl -pi -e "s/(\w.*)(# Default)/# \$1\$2/g" ./xkeysnail-config/kinto.py.new
fi

if [[ $1 == "1" || $1 == "2" || $1 == "3" || $1 == "winmac" || $1 == "mac" || $1 == "chromebook" ]]; then
	mv ./xkeysnail-config/kinto.py.new ~/.config/kinto/kinto.py
	sudo mv ./xkeysnail-config/xkeysnail.service.new /etc/systemd/system/xkeysnail.service 
	git clone --depth 1 https://github.com/rbreaves/xkeysnail.git
	cd xkeysnail
	sudo pip3 install --upgrade .
	sudo systemctl enable xkeysnail
	sudo systemctl daemon-reload
	sudo systemctl start xkeysnail

	echo "Adding xhost fix..."

	# KDE startup - xhost fix
	cp ./xkeysnail-config/xkeysnail.desktop ~/.config/autostart/xkeysnail.desktop

	LINE='xhost +SI:localuser:root'

	if [ ! -e "~/.xprofile" ]; then
		# Ubuntu xhost fix
		echo "$LINE" > ~/.xprofile
		# echo "$LINE" > ~/.xinitrc
	fi
	# Ubuntu xhost fix
	grep -qF -- "$LINE" ~/.xprofile || echo "$LINE" >> ~/.xprofile
	# KDE xhost fix
	# grep -qF -- "$LINE" ~/.bashrc || echo "$LINE" >> ~/.bashrc
	# grep -qF -- "$LINE" ~/.xinitrc || echo "$LINE" >> ~/.xinitrc

	# remove kintox11 login startup
	rm ~/.config/autostart/kinto.desktop
else
	echo "Expected argument was not provided"
fi


