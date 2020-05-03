#!/bin/bash

if [ -f /home/{username}/.config/systemd/user/keyswap.timer ]; then
	systemctl --user stop keyswap.timer >/dev/null 2>&1
	systemctl --user disable keyswap.timer >/dev/null 2>&1
fi
if [ -f /home/{username}/.config/systemd/user/keyswap.service ]; then
	systemctl --user stop keyswap >/dev/null 2>&1
	systemctl --user disable keyswap >/dev/null 2>&1
fi

# export DISPLAY={displayid};/usr/bin/xhost +SI:localuser:root
mkdir -p /tmp/kinto/xkeysnail
cp /home/{username}/.config/kinto/kinto.py /tmp/kinto/xkeysnail/kinto.py