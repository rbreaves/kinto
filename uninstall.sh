#!/bin/bash

systemctl --user stop keyswap 2>/dev/null
systemctl --user disable keyswap
systemctl --user stop keyswap.timer 2>/dev/null
systemctl --user disable keyswap.timer
rm ~/.config/systemd/user/keyswap.service
rm ~/.config/systemd/user/keyswap.timer
rm -rf ~/.config/autostart/kinto.desktop
rm -rf ~/.config/kinto
rm -rf ~/.xkb
systemctl daemon-reload
sed -i '/xkb/d' ~/.Xsession 2>/dev/null