#!/bin/bash
mkdir -p ~/.xkb/{keymap,symbols,types}
cp ./.xkb/symbols/mac_onelvl ~/.xkb/symbols/mac_onelvl
cp ./.xkb/types/mac_onelvl ~/.xkb/types/mac_onelvl
setxkbmap -option
setxkbmap -print > ~/.xkb/keymap/kbd.mac.onelvl
line=$(cat ~/.xkb/keymap/kbd.mac.onelvl | grep -n 'xkb_symbols' | cut -f1 -d:)
sed -ie "${line}s/)\"/)+altwin(ctrl_alt_win)+mac_onelvl(mac_onelvlsym)\"/g" ~/.xkb/keymap/kbd.mac.onelvl
