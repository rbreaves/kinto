#!/usr/bin/env bash
dbus-monitor --session "type='signal',interface='org.gnome.SessionManager.Logout'" | grep '1' |
while read x; do
  # echo "$x"
  sudo systemctl stop xkeysnail
  exit 0
done
