#!/bin/bash

systemctl --user stop keyswap
systemctl --user disable keyswap
rm -rf ~/.config/autostart/keyswap.sh
rm -rf ~/.config/xactive.sh
rm -rf ~/.xkb

sed -i '/xkb/d' ~/.Xsession