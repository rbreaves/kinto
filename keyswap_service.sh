#!/bin/bash

swapcmd="\/bin\/bash\ \/home\/`whoami`\/.config\/kinto\/xactive.sh"
mkdir -p ~/.config/systemd/user
mkdir -p ~/.config/autostart
cp ./system-config/keyswap.service ~/.config/systemd/user/keyswap.service
cp ./system-config/keyswap.timer ~/.config/systemd/user/keyswap.timer
cp ./kintox11/binary/kintox11 ~/.config/kinto/kintox11
cp ./system-config/xactive.sh ~/.config/kinto/xactive.sh
sed -i "s/{username}/`whoami`/g" ~/.config/systemd/user/keyswap.service
sed -i "s/ExecStart=/ExecStart=${swapcmd}/g" ~/.config/systemd/user/keyswap.service
systemctl --user enable keyswap.timer
systemctl --user start keyswap.timer