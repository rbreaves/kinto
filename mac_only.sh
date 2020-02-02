#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/mac_gui ~/.xkb/symbols/mac_gui
cp ./.xkb/types/mac_gui ~/.xkb/types/mac_gui
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui
setxkbmap -print > ~/.xkb/keymap/kbd.mac.term
line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/\"/+ctrl(swap_lwin_lctl)+ctrl(swap_rwin_rctl)+mac_gui(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.mac.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:)
sed -ie "${line}s/\"/+mac_gui(addmac_levels)\"/2" ~/.xkb/keymap/kbd.mac.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.mac.term | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/\"/+altwin(alt_super_win)+mac_term(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.mac.term
