#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/chromebook ~/.xkb/symbols/chromebook
cp ./.xkb/symbols/mac_levels ~/.xkb/symbols/mac_levels
cp ./.xkb/types/mac_levels ~/.xkb/types/mac_levels
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.chromebook.gui
line=$(cat ~/.xkb/keymap/kbd.chromebook.gui | grep -n 'xkb_types' | cut -f1 -d:)
sed -ie "${line}s/\"/)+mac_levels(addmac_levels)\"/2" ~/.xkb/keymap/kbd.chromebook.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.chromebook.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/\"/+chromebook(swap_lalt_lctrl)+mac_levels(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.chromebook.gui
