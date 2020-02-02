#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/chromebook ~/.xkb/symbols/chromebook
cp ./.xkb/symbols/mac_gui ~/.xkb/symbols/mac_gui
cp ./.xkb/types/mac_gui ~/.xkb/types/mac_gui
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.chromebook.gui
setxkbmap -print > ~/.xkb/keymap/kbd.chromebook.term
line=$(cat ~/.xkb/keymap/kbd.chromebook.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/\"/+chromebook(swap_lalt_lctrl)+mac_gui(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.chromebook.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.chromebook.gui | grep -n 'xkb_types' | cut -f1 -d:)
sed -ie "${line}s/\"/+mac_gui(addmac_levels)\"/2" ~/.xkb/keymap/kbd.chromebook.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.chromebook.term | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/\"/+altwin(swap_alt_win)+mac_term(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.chromebook.term
