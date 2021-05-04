#!/usr/bin/env bash

action=$1

saveClipboard=$(xclip -selection clipboard -o)
echo "" | xclip -i -selection clipboard

if [ "$action" == "Left" ] || [ "$action" == "Undo" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers Shift+Home ctrl+c Home
	firstClipboard=$(xclip -selection clipboard -o)
	if [ "$firstClipboard" == "" ];then
		xdotool getactivewindow key --delay 40 --clearmodifiers Shift+Right ctrl+c Home
		firstClipboard=$(xclip -selection clipboard -o)
		if [ "$firstClipboard" == "" ];then
			xdotool getactivewindow key --delay 24 --clearmodifiers bar Shift+Left ctrl+x
			firstClipboard=$(xclip -selection clipboard -o)
		fi
	fi
	echo "" | xclip -i -selection clipboard
	xdotool getactivewindow key --clearmodifiers Shift+Right ctrl+c Home
	if [ "${firstClipboard:0:1}" == "$(xclip -selection clipboard -o)" ];then
		echo "" | xclip -i -selection clipboard
	fi

fi

if [ "$action" == "Right" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers Shift+End ctrl+c
	firstClipboard=$(xclip -selection clipboard -o | tr -d /)
	if [ "$firstClipboard" == "" ];then
		xdotool getactivewindow key --delay 40 --clearmodifiers Left Shift+Right ctrl+c
		firstClipboard=$(xclip -selection clipboard -o | tr -d /)
		if [ "$firstClipboard" == "" ];then
			xdotool getactivewindow key --delay 24 --clearmodifiers bar Shift+Left ctrl+x
			firstClipboard=$(xclip -selection clipboard -o | tr -d /)
		fi
	fi
	if [ "$firstClipboard" != "" ];then
		xdotool getactivewindow key --clearmodifiers Right
	fi
	echo "" | xclip -i -selection clipboard
	xdotool getactivewindow key --clearmodifiers Shift+Left ctrl+c
	if [ "${firstClipboard: -1}" == "$(xclip -selection clipboard -o)" ];then
		echo "" | xclip -i -selection clipboard
		xdotool getactivewindow key --clearmodifiers Right
	fi
fi

newClipboard=$(xclip -selection clipboard -o)

# echo ${#firstClipboard}
# echo "$firstClipboard""-"
# echo "first"
# echo ${#newClipboard}
# echo "$newClipboard""-"
# echo "hello"


if [ "$action" == "Left" ] && ([ "$firstClipboard" == "" ] || [ "$newClipboard" != "" ]);then
	xdotool getactivewindow key --clearmodifiers alt+Left
fi

if [ "$action" == "Right" ] && ([ "$firstClipboard" == "" ] || [ "$newClipboard" != "" ]);then
	xdotool getactivewindow key --clearmodifiers alt+Right
elif [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers End
fi

if [ "$action" == "Undo" ] && ([ "$firstClipboard" != "" ] && [ "$newClipboard" == "" ]);then
	xdotool getactivewindow key --delay 24 --clearmodifiers ctrl+z
elif [ "$action" == "Undo" ];then
	xdotool getactivewindow key ctrl+Shift+t
fi

echo $saveClipboard | xclip -i -selection clipboard