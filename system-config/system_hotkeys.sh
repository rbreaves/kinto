#!/bin/bash

if [ "$1" = "term" ];
	then
	gsettings set org.gnome.desktop.wm.keybindings switch-applications "['<Shift><Control>Tab']"
	gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward "['']"
else
	gsettings set org.gnome.desktop.wm.keybindings switch-applications "['<Control>Tab']"
	gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward "['<Shift><Control>Tab']"
fi
