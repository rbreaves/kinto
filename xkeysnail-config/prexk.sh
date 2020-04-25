#!/bin/bash

if systemctl -q --user is-enabled keyswap.timer; then
	systemctl --user stop keyswap.timer
	systemctl --user disable keyswap.timer
fi
if systemctl -q --user is-active keyswap; then
	systemctl --user stop keyswap
fi
if systemctl -q --user is-enabled keyswap; then
	systemctl --user disable keyswap
fi

# export DISPLAY={displayid};/usr/bin/xhost +SI:localuser:root
mkdir -p /tmp/kinto
cp /home/{username}/.config/kinto/kinto.py /tmp/kinto/kinto.py