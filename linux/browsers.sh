#!/usr/bin/env bash

action=$1

saveClipboard=$(xclip -selection clipboard -o)
echo "$saveClipboard"
echo "" | xclip -i -selection clipboard
# --delay 12
xdotool getactivewindow key --clearmodifiers Left Left Right Shift+Right ctrl+c Right
newClipboard=$(xclip -selection clipboard -o)


if [ "$newClipboard" == "" ] && [ "$action" == "Left" ];then
	xdotool getactivewindow key --clearmodifiers alt+Left
elif [ "$action" == "Left" ];then
	xdotool getactivewindow key --clearmodifiers Home
fi

if [ "$newClipboard" == "" ] && [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers alt+Right
elif [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers End
fi

if [ "$newClipboard" == "" ] && [ "$action" == "Undo" ];then
	xdotool getactivewindow key ctrl+Shift+t
elif [ "$action" == "Undo" ];then
	xdotool getactivewindow key --clearmodifiers ctrl+z
fi

echo $saveClipboard | xclip -i -selection clipboard