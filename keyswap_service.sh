#!/bin/bash

systemctl --user stop keyswap >/dev/null 2>&1
systemctl --user disable keyswap >/dev/null 2>&1
systemctl --user stop keyswap.timer >/dev/null 2>&1
systemctl --user disable keyswap.timer >/dev/null 2>&1
swapcmd="\/home\/`whoami`\/.config\/kinto\/xactive.sh"
mkdir -p ~/.config/systemd/user
mkdir -p ~/.config/autostart
cp ./system-config/keyswap.service ~/.config/systemd/user/keyswap.service
cp ./system-config/kinto.desktop ~/.config/autostart/kinto.desktop
cp ./kintox11/binary/kintox11 ~/.config/kinto/kintox11
cp ./system-config/xactive.sh ~/.config/kinto/xactive.sh
sed -i "s/{username}/`whoami`/g" ~/.config/systemd/user/keyswap.service
sed -i "s/ExecStart=/ExecStart=${swapcmd}/g" ~/.config/systemd/user/keyswap.service
systemctl --user daemon-reload
systemctl --user enable keyswap
systemctl --user start keyswap
