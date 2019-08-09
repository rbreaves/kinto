#!/bin/bash
# How to add more terminal editors
# run this command while using the terminal
# and add the name to class_name
# xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) WM_CLASS
class_name='konsole\|Gnome-terminal\|terminator\|sakura\|guake\|tilda\|xterm\|eterm'

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
elif [[ "$systemtype" == "mac_only" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY"
	check_gt="setxkbmap -query | grep -v 'alt_super_win' 1>/dev/null"
	check_tg="setxkbmap -query | grep -q 'alt_super_win'"
elif [[ "$swapbehavior" == "both_mac" ]]; then
	swapcmd_gui="setxkbmap -option;setxkbmap -option ctrl:swap_lwin_lctl; xkbcomp -w0 -i $internalid -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
	swapcmd_term="setxkbmap -option;setxkbmap -device $internalid -option 'altwin:swap_alt_win'"
	check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
	check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
elif [[ "$swapbehavior" == "both_win" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY; setxkbmap -device $usbid -option altwin:ctrl_alt_win"
	fallbackcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
	check_gt="setxkbmap -query | grep -q 'ctrl_alt_win'"
	check_tg="setxkbmap -query | grep -v 'ctrl_alt_win' 1>/dev/null"
elif [[ "$swapbehavior" == "none" ]]; then
	swapcmd_gui="setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY"
	check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
	check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
fi

# echo "$systemtype $swapbehavior"
# echo "$swapcmd_gui"

eval "$swapcmd_gui"

# regex for extracting hex id's
grep_id='0[xX][a-zA-Z0-9]\+'

#Storing timestamp and will use timediff to prevent xprop duplicates
timestp=$(date +%s)

xprop -spy -root _NET_ACTIVE_WINDOW | grep --line-buffered -o $grep_id |
while read -r id; do
	class="`xprop -id $id WM_CLASS | grep $class_name`"
	newtime=$(date +%s)
	timediff=$((newtime-timestp))
	if [ $timediff -gt 0 ]; then
		if [ -n "$class" ]; then
			# Set keymap for terminal, Alt is Super, Ctrl is Ctrl, Super is Alt
			eval "$check_gt"
			echo $?
			if [ $? -eq 0 ]; then
				echo "internal gui to term"
				eval "$swapcmd_term"

				# Quick hack, will want to refactor later
				# just resets required checks, for chromebooks that
				# use usb windows keyboards
				if [[ "$swapbehavior" == "both_win" ]]; then
					check_gt="setxkbmap -query | grep -q 'ctrl_alt_win'"
					check_tg="setxkbmap -query | grep -v 'ctrl_alt_win' 1>/dev/null"
				fi
			fi
		else
			# Set keymap for gui, Alt is Ctrl,Super is Alt, Ctrl is Super
			eval "$check_tg"
			echo $?
			if [ $? -eq 0 ]; then
				echo "internal term to gui"
				eval "$swapcmd_gui"
				if [ $? -eq 0 ] && [[ "$swapbehavior" == "both_win" ]]; then
					eval "$fallbackcmd_gui"
					check_gt="setxkbmap -query | grep -v 'swap_alt_win' 1>/dev/null"
					check_tg="setxkbmap -query | grep -q 'swap_alt_win'"
				fi
			fi
		fi
		timestp=$(date +%s)
	fi
done