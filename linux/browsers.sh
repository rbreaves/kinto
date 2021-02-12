#!/usr/bin/env bash

action=$1

saveClipboard=$(xclip -selection clipboard -o)
echo "" | xclip -i -selection clipboard
if [ "$action" == "Left" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers End bar Shift+Left ctrl+x
fi
if [ "$action" == "Right" ];then
	xdotool getactivewindow key --delay 40 --clearmodifiers Home bar Shift+Left ctrl+x
fi
if [ "$action" == "Undo" ];then
	xdotool getactivewindow key --delay 24 --clearmodifiers bar Shift+Left ctrl+x
	sleep 0.1
fi

newClipboard=$(xclip -selection clipboard -o)

# echo "$newClipboard"
# echo "hello"

if [ "$newClipboard" != "|" ] && [ "$action" == "Left" ];then
	xdotool getactivewindow key --clearmodifiers alt+Left
elif [ "$action" == "Left" ];then
	xdotool getactivewindow key --clearmodifiers Home
fi

if [ "$newClipboard" != "|" ] && [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers alt+Right
elif [ "$action" == "Right" ];then
	xdotool getactivewindow key --clearmodifiers End
fi

if [ "$newClipboard" != "|" ] && [ "$action" == "Undo" ];then
	xdotool getactivewindow key ctrl+Shift+t
elif [ "$action" == "Undo" ];then
	xdotool getactivewindow key --delay 24 --clearmodifiers ctrl+z ctrl+z ctrl+z
fi

echo $saveClipboard | xclip -i -selection clipboard