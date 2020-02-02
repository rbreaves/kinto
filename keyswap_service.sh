#!/bin/bash

swapcmd="\/bin\/bash\ \/home\/`whoami`\/.config\/kinto\/kintox11"
mkdir -p ~/.config/systemd/user
mkdir -p ~/.config/autostart
cp ./system-config/keyswap.service ~/.config/systemd/user/keyswap.service
cp ./system-config/keyswap.sh ~/.config/autostart/keyswap.sh
cp ./kintox11/binary/kintox11_ubuntu19-10 ~/.config/kinto/kintox11
sed -i "s/{username}/`whoami`/g" ~/.config/systemd/user/keyswap.service
sed -i "s/ExecStart=/ExecStart=${swapcmd}/g" ~/.config/systemd/user/keyswap.service
systemctl --user enable keyswap
systemctl --user start keyswap