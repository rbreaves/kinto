#!/bin/bash
class_name='konsole'

internalkb=$1
internalid=$2
usbkb=$3
usbid=$4
swapbehavior=$5

# echo $1 $2 $3 $4

internalgui="setxkbmap -device $internalid -option "
internalterm="$internalgui"
usbgui="setxkbmap -device $usbid -option "
usbterm="$usbgui"

if [[ $internalkb == "windows" ]]; then
	internalgui+="altwin:ctrl_alt_win"
	internalterm+="altwin:swap_alt_win"
	internalgrep_term="-q ctrl_alt_win"
	internalgrep_gui="-v ctrl_alt_win\ 1>/dev/null"
elif [[ $internalkb == "chromebook" ]]; then
	internalgui="xkbcomp -w0 -I$HOME/.xkb -i $internalid ~/.xkb/keymap/kbd.gui $DISPLAY"
	internalterm+="altwin:swap_lalt_lwin"
	# internalgrep_term="-vq swap_lalt_lwin"
	internalgrep_term="-q swap_lalt_lwin"
	internalgrep_gui="-v swap_lalt_lwin 1>/dev/null"
elif [[ $internalkb == "mac" ]]; then
	internalgui+="ctrl:swap_lwin_lctl"
	#mac term is blank
	internalterm=""
	internalgrep_term="-q swap_lwin_lctl"
	internalgrep_gui="-v swap_lwin_lctl 1>/dev/null"
fi

if [[ $usbkb == "windows" ]]; then
	usbgui+="altwin:ctrl_alt_win"
	usbterm+="altwin:swap_alt_win"
	usbgrep_term="-q ctrl_alt_win"
	usbgrep_gui="-v ctrl_alt_win 1>/dev/null"
elif [[ $usbkb == "chromebook" ]]; then
	usbgui="xkbcomp -w0 -I$HOME/.xkb -i $usbid ~/.xkb/keymap/kbd.gui $DISPLAY"
	usbterm+="altwin:swap_lalt_lwin"
	usbgrep_term="-q swap_lalt_lwin"
	usbgrep_gui="-v swap_lalt_lwin 1>/dev/null"
elif [[ $usbkb == "mac" ]]; then
	usbgui+="ctrl:swap_lwin_lctl"
	#mac term is blank
	usbterm=""
	usbgrep_term="-q swap_lwin_lctl"
	usbgrep_gui="-v swap_lwin_lctl 1>/dev/null"
fi

# echo "$internalgui"
# echo "$internalterm"

# echo "$usbgui"
# echo "$usbterm"

# exit

# regex for extracting hex id's
grep_id='0[xX][a-zA-Z0-9]\{7\}'

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
			if [[ $internalid -gt 0 ]]; then
				echo "internal gui to term"
				echo "$internalgrep_gui"
				eval "setxkbmap -query | grep $internalgrep_gui"
				if [ $? -eq 0 ]; then
					echo "* inside internal gui to term"
					echo "* $internalterm"
					eval setxkbmap -device $internalid -option
					eval $internalterm
				fi
			fi
			if [[ $usbid -gt 0 ]]; then
				echo "usb gui to term"
				echo "$usbgrep_gui"
				eval "setxkbmap -query | grep $usbgrep_gui"
				if [ $? -eq 0 ]; then
					echo "* inside usb gui to term"
					echo "* $usbterm"
					eval setxkbmap -device $usbid -option
					eval $usbterm
				fi
			fi
		else
			# Set keymap for gui, Alt is Ctrl,Super is Alt, Ctrl is Super
			if [[ $internalid -gt 0 ]]; then
				echo "internal term to gui"
				echo "$internalgrep_term"
				eval "setxkbmap -query | grep $internalgrep_term"
				if [ $? -eq 0 ]; then
					echo "** inside internal term to gui"
					echo "** $internalgui"
					eval "setxkbmap -device $internalid -option"
					eval "$internalgui"
				fi
			fi
			if [[ $usbid -gt 0 ]]; then
				echo "usb term to gui"
				echo "$usbgrep_term"
				eval "setxkbmap -query | grep $usbgrep_term"
				if [ $? -eq 0 ]; then
					echo "** inside usb term to gui"
					eval setxkbmap -device $usbid -option
					eval $usbgui
				fi
			fi
		fi
		timestp=$(date +%s)
	fi
done