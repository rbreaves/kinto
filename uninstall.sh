#!/bin/bash

systemctl --user stop keyswap
systemctl --user disable keyswap
rm -rf ~/.config/autostart/kinto.desktop
rm -rf ~/.config/kinto
rm -rf ~/.xkb

sed -i '/xkb/d' ~/.Xsession