#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/mac_gui ~/.xkb/symbols/mac_gui
cp ./.xkb/types/mac_term ~/.xkb/types/mac_term
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui
line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+altwin(ctrl_alt_win)+mac_gui(mac_levelssym)\"/g" ~/.xkb/keymap/kbd.mac.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+mac_gui(addmac_levels)\"/g" ~/.xkb/keymap/kbd.mac.gui
