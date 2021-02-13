#!/usr/bin/env bash

action=$1

saveClipboard=$(xclip -selection clipboard -o)
echo "" | xclip -i -selection clipboard
if [ "$action" == "Left" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers End Shift+Left ctrl+c
	firstClipboard=$(xclip -selection clipboard -o)
	if [ "${#firstClipboard}" > 1 ];then
		firstClipboard=${firstClipboard: -1}
	fi
	echo "" | xclip -i -selection clipboard
	xdotool getactivewindow key --delay 24 --clearmodifiers Left Shift+Right ctrl+c Right
fi
if [ "$action" == "Right" ] || [ "$action" == "Undo" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers Home Shift+Right ctrl+c
	firstClipboard=$(xclip -selection clipboard -o)
	if [ "${#firstClipboard}" > 1 ];then
		firstClipboard=${firstClipboard:0:1}
	fi
	echo "" | xclip -i -selection clipboard
	xdotool getactivewindow key --delay 24 --clearmodifiers Right Shift+Left ctrl+c Left
fi

newClipboard=$(xclip -selection clipboard -o)

# echo ${#firstClipboard}
# echo "$firstClipboard""-"
# echo "first"
# echo ${#newClipboard}
# echo "$newClipboard""-"
# echo "hello"

if [ "$action" == "Undo" ] && [ "$newClipboard" == "" ] && [ "$firstClipboard" == "" ];then
	xdotool getactivewindow key --delay 24 --clearmodifiers bar Shift+Left ctrl+c Left
	firstClipboard=$(xclip -selection clipboard -o)
	echo "" | xclip -i -selection clipboard
	xdotool getactivewindow key --delay 24 --clearmodifiers Shift+Right ctrl+x
	newClipboard=$(xclip -selection clipboard -o)
	if [ "$newClipboard" != "" ] && [ "$firstClipboard" != "" ];then
		xdotool getactivewindow key --delay 24 --clearmodifiers ctrl+z ctrl+z
	fi
fi

if [ "$action" == "Left" ] && [ "$newClipboard" != "" ] && [ "$newClipboard" == "$firstClipboard" ];then
	xdotool getactivewindow key --clearmodifiers Home
elif [ "$action" == "Left" ];then
	xdotool getactivewindow key --clearmodifiers alt+Left
fi

if [ "$action" == "Right" ] && [ "$newClipboard" != "" ] && [ "$newClipboard" == "$firstClipboard" ];then
	xdotool getactivewindow key --clearmodifiers End
elif [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers alt+Right
fi

if [ "$action" == "Undo" ] && [ "$newClipboard" != "" ] && [ "$newClipboard" == "$firstClipboard" ];then
	xdotool getactivewindow key --delay 24 --clearmodifiers ctrl+z
elif [ "$action" == "Undo" ];then
	xdotool getactivewindow key ctrl+Shift+t
fi

echo $saveClipboard | xclip -i -selection clipboard