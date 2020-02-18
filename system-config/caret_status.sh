#!/bin/bash

mkdir -p /tmp/kinto

IBUSADD=$(cat ~/.config/ibus/bus/`ls ~/.config/ibus/bus -1rt | tail -n1` | awk -F'IBUS_ADDRESS=' '{print $2}' | xargs)
dbus-monitor --address $IBUSADD "path='/org/freedesktop/IBus/Panel',interface='org.freedesktop.IBus.Panel',member='FocusOut'" 2> /dev/null | grep --line-buffered -o -P '(?<=object path \"/org/freedesktop/IBus/InputContext_).*(?=[\"])' |
while read ln
do
  printf '%s\n' "$ln" > /tmp/kinto/caret
done
