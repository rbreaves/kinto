#!/bin/bash

setxkbmap -option
# force command to run silently and report true
killall xbindkeys > /dev/null 2>&1 || :
# rm /tmp/kinto/caret

gsettings set org.gnome.desktop.wm.keybindings switch-applications "['<Alt>Tab']"
gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward "['<Shift><Alt>Tab']"
pkill -f /.config/kinto/xactive.sh