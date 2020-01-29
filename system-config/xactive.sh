#!/bin/bash

systemtype=$1
internalid=$2
usbid=$3
swapbehavior=$4

# echo $1 $2 $3 $4

swapcmd_term="setxkbmap -option;setxkbmap -option altwin:swap_alt_win"
fallbackcmd_gui=""
if [[ "$systemtype" == "windows" || "$systemtype" == "mac" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY"
	check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
	check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
# mac_only is for apple keyboards without an apple hid driver
elif [[ "$systemtype" == "mac_only" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY"
	swapcmd_term="setxkbmap -option"
# Chromebook options
elif [[ "$swapbehavior" == "both_mac" ]]; then
	swapcmd_gui="setxkbmap -option;setxkbmap -option ctrl:swap_lwin_lctl; xkbcomp -w0 -i $internalid -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
	swapcmd_term="setxkbmap -option;setxkbmap -device $internalid -option 'altwin:swap_alt_win'"
elif [[ "$swapbehavior" == "both_win" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY; setxkbmap -device $usbid -option altwin:ctrl_alt_win"
	fallbackcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
elif [[ "$swapbehavior" == "none" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
fi

eval "$swapcmd_gui"

# If running gnome this will disable the overlay-key mapping
gsettings set org.gnome.mutter overlay-key ''
kwriteconfig5 --file ~/.config/kwinrc --group ModifierOnlyShortcuts --key Meta ""
qdbus org.kde.KWin /KWin reconfigure

./kintox11 |
while read -r id; do
	if [[ "$id" == "term" ]]; then
		echo "internal gui to term"
		eval "$swapcmd_term"
		
		# Gnome - Set Activities Overview
		gsettings set org.gnome.desktop.wm.keybindings panel-main-menu "['<Super>Space']"
		# ~/.config/kglobalshortcutsrc
		# activate widget 78=Super+Space,none,Activate Application Launcher Widget
		# kquitapp kglobalaccel && sleep 2s && kglobalaccel5&
		# kquitapp5 plasmashell && kstart5 plasmashell
	fi

	if [[ "$id" == "gui" ]]; then
		echo "internal term to gui"
		eval "$swapcmd_gui"

		# Gnome - Set Activities Overview
		gsettings set org.gnome.desktop.wm.keybindings panel-main-menu "['<Ctrl>Space']"
		# ~/.config/kglobalshortcutsrc
		# activate widget 78=Ctrl+Space,none,Activate Application Launcher Widget
		# kquitapp kglobalaccel && sleep 2s && kglobalaccel &

		# # Fallback code
		# if [ $? -eq 0 ] && [[ "$swapbehavior" == "both_win" ]]; then
		# 	eval "$fallbackcmd_gui"
		# 	check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
		# 	check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
		# fi
	fi

done