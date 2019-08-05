#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/chromebook ~/.xkb/symbols/chromebook
cp ./.xkb/symbols/mac_gui ~/.xkb/symbols/mac_gui
cp ./.xkb/types/mac_term ~/.xkb/types/mac_term
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.chromebook.gui
line=$(cat ~/.xkb/keymap/kbd.chromebook.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+chromebook(swap_lalt_lctrl)+mac_gui(mac_onelvlsym)\"/g" ~/.xkb/keymap/kbd.chromebook.gui
sleep 1
line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+mac_gui(addmac_levels)\"/g" ~/.xkb/keymap/kbd.chromebook.gui
