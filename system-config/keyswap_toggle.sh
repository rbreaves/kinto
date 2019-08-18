#!/bin/bash
# Manual keyswap
systemtype=$1
internalid=$2
usbid=$3
swapbehavior=$4

swapcmd_term="setxkbmap -option;setxkbmap -option altwin:swap_alt_win"
fallbackcmd_gui=""
if [[ "$systemtype" == "windows" || "$systemtype" == "mac" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY"
elif [[ "$systemtype" == "mac_only" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY"
# Chromebook keyboard options
elif [[ "$swapbehavior" == "both_mac" ]]; then
	swapcmd_gui="setxkbmap -option;setxkbmap -option ctrl:swap_lwin_lctl; xkbcomp -w0 -i $internalid -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
	swapcmd_term="setxkbmap -option;setxkbmap -device $internalid -option 'altwin:swap_alt_win'"
elif [[ "$swapbehavior" == "both_win" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY; setxkbmap -device $usbid -option altwin:ctrl_alt_win"
	fallbackcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
elif [[ "$swapbehavior" == "none" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
fi

if [[ "$swapbehavior" == "both_win" ]]; then
	check=`setxkbmap -query | grep -q 'ctrl_alt_win'; echo $?`
else
	check=`setxkbmap -query | grep -c 'swap_alt_win'`
fi

echo $check
if [ $check -eq 0 ]; then
	echo "internal gui to term"
	eval "$swapcmd_term"

	# Quick hack, will want to refactor later
	# just resets required checks, for chromebooks that
	# use usb windows keyboards
	if [[ "$swapbehavior" == "both_win" ]]; then
		check_gt="setxkbmap -query | grep -q 'ctrl_alt_win'"
		check_tg="setxkbmap -query | grep -v 'ctrl_alt_win' 1>/dev/null"
	fi
else
	echo "internal term to gui"
	eval "$swapcmd_gui"
	
	if [ $? -eq 0 ] && [[ "$swapbehavior" == "both_win" ]]; then
		eval "$fallbackcmd_gui"
		check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
		check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
	fi
fi