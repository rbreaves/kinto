#!/bin/bash

xkeycount=$(pgrep 'xkeysnail' | wc -l)

if [[ $xkeycount -le 1 ]]; then
	# No dups found
	exit 0
fi

while ! zenity --entry --title="Kinto Duplicates" --text="Type Password to end duplicates:" --hide-text| sudo -S cat /dev/null >/dev/null; do
if ! $(zenity --question --text="Wrong password, try again?"); then
	# Dups still exist
	exit 1
fi
done
# pgrep 'xkeysnail' | head -n -1 | xargs -r -n1 sudo kill
pgrep 'xkeysnail' | xargs -r -n1 sudo kill
sudo -K # remove privilege
# No dups should exist
exit 0