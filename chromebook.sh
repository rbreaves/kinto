#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols}
cp ./.xkb/symbols/chromebook ~/.xkb/symbols/chromebook
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.gui
line=$(cat ~/.xkb/keymap/kbd.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+chromebook(swap_lalt_lctrl)\"/g" ~/.xkb/keymap/kbd.gui
