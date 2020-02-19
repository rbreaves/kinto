#!/bin/bash

setxkbmap -option
# force command to run silently and report true
killall xbindkeys > /dev/null 2>&1 || :
# rm /tmp/kinto/caret
