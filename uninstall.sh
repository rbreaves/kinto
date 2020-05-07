#!/bin/bash
# Undo Apple keyboard cmd & alt swap
if test -f "/sys/module/hid_apple/parameters/swap_opt_cmd" && [ `cat /sys/module/hid_apple/parameters/swap_opt_cmd` == "1" ]; then
	echo '0' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd
	echo 'options hid_apple swap_opt_cmd=0' | sudo tee -a /etc/modprobe.d/hid_apple.conf
	sudo update-initramfs -u -k all
fi
systemctl --user stop keyswap 2>/dev/null
systemctl --user disable keyswap
systemctl --user stop keyswap.timer 2>/dev/null
systemctl --user disable keyswap.timer
rm ~/.config/systemd/user/keyswap.service
rm ~/.config/systemd/user/keyswap.timer
rm -rf ~/.config/autostart/kinto.desktop
rm -rf ~/.config/kinto
rm -rf ~/.xkb
sudo systemctl daemon-reload
sed -i '/xkb/d' ~/.Xsession 2>/dev/null
exit 0