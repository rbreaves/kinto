# Kinto

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases)

\- A better linux keyboard layout for professional mac users \-

Memory muscle matters for programmers and developers.

If it happens on your mac keyboard then it should happen the same in linux.

## What does this do exactly?

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/kinto-demo.gif)

Remaps your keyboard to behave more like you're on a mac again and below is how the keymap will behave. (Note: Kinto does support the remapping of Apple keyboards just fine, so you can safely ignore how I describe the keymapping below - since that is based on PC/Windows keyboards.)

- Normal apps - Alt will be Ctrl, Win/Super will be Alt, Ctrl will be Win/Super

- Terminal apps (optional) - Alt will be Win/Super, Win/Super will be Alt, Ctrl will be Ctrl

- New Features - Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

- ~~Modify existing Terminal app keymap profiles (optional and with confirmation) - Copy, Paste, New Tab, etc will be remapped to use Win/Super in the physical Command (or Alt key) position.~~

## What does Kinto require?

- Python
- systemd
- x11

Any Linux distro that uses systemd. Compatibility can easily be expanded, but currently I am only writing and testing this with systemd services.

X11 is the only other requirement. Wayland can be supported, but will require a replacement for xprop - any app or DE plugin that can be made aware of the active application name and trigger scripts is sufficient. If this alternative is found then it may also replace xprop, assuming it is also compatible under x11.

## How to install

1. clone this repo
```
git clone https://github.com/rbreaves/kinto.git
```
2. Install python3 and xprop (If needed)

Debian or Ubuntu 16.04 or 18.04
```
sudo apt update
sudo apt install python3 x11-utils
```

3. Follow the prompts and the script will guide you through the rest of the setup.
```
./install.py
```

## How to Control Kinto

Under systemd this is how you control Kinto.

Status
```
systemctl --user status keyswap
```

Stop
```
systemctl --user stop keyswap
```

Start
```
systemctl --user start keyswap
```

Enable
```
systemctl --user enable keyswap
```

Disable
```
systemctl --user disable keyswap
```

## Manually Toggling Kinto via hotkey

Occasionally you may run into the Kinto keyswap not swapping your keys, this ought to be extremely rare, but if you need to manaully run the keyswap via a hotkey then you may. Of course you can also just toggle between a terminal app and any other app as well, but if you need to swap the keymap in other apps or websites, like shortcutfoo for learning macos style hotkeys, then this will be useful.

I have not yet automated this, due to the wide range of DE's and each one needing the shortcut setup to be a little different.

Here's what you will want to do however.

1. Run a Status check on Kinto
```
systemctl --user status keyswap
```
and pay attention to the values that come after xactive.sh in the output.

2. Run the following command, replacing the 4 values below with yours.
```
~/.config/keyswap_toggle.sh win 0 0 0
```
3. Run this command a few more times and make sure it is swapping between "gui to term" and "term to gui"
4. Go into the DE system settings and bind the hotkeys you want to use to activate it. You may want to select two hotkey combinations, so that if you are using your modifier keys you will be using the same physical keys to activate the script.

Note: If I automate this later then the shortcut keys I plan to use are Ctrl+Alt+0 (and Alt+Super+0).

## Learning macOS style hotkeys on Linux

If you are interested in that then websites like https://www.shortcutfoo.com would be highly useful and it is completely doable on linux as long as you use the terminal style keymap while using your browser. I have not found a way to make it work under Firefox, but it does work great under Chrome, with or without a User Agent plugin.

To make sure you are in the terminal style keymap you can just simply open the terminal and turn off the kinto service, and then switch back to Chrome.
```
systemctl --user stop keyswap
```

or alternatively, you can follow the instructions about how to manually trigger a toggle of the keyswap.

## Troubleshooting
If your keyboard is not being autodetected and configured then please run `xinput list`, if you are on linux, and copy the output into a ticket under issues.

## Language Support
As far as I know this solution should work fine on all languages, but I am not able to test this on anything besides US based keyboards. The custom keymaps themselves are moduler, however if you find a problem or want to add needed language support then you can create new keymap files under the .xkb directory, just follow a similar scheme as the existing one and additional modifications can be made to mac_wordwise.sh to support additional languages during install.

If you would like to attempt adding additional custom keymaps then I strongly recommend reading Glen Whitney's post here.
https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste


## Known Issues

### USB Hubs

No longer an issue. If the Apple hid_apple driver is not detected, when an Apple keyboard has been selected, then the installer will only install a keymap that will work with Apple keyboards that have no driver attached. Otherwise a keymap that is compatible with both Windows and Apple keyboards will be applied.

### KDE with Konsole or QT5 apps may block Super+ custom keymaps

This only applies to xkb file based keymaps - intended to be global key remapping, not app specific keymaps in QT5 or konsole. App specific keymaps will continue to work fine.

In the macterm branch you will find a WIP, it is possible to remap Super+T to something like Ctrl+Shift+T using xkbcomp, so that remapping certain defaults in most Terminal apps would not be required. The issue however is that KDE and Konsole (or QT5 apps?) appear to have a conflict with the custom keymap I created for Super. Until a resolution is found this feature will not be a default or optional to install.

If anyone finds a solution then please contact me, create an issue or submit a pull request and I will merge it - the custom Terminal keymaps have already been made and exist in all branches.

## Debugging

If you would like you can disable the Kinto keyswap service and run xactive.sh directly so that you can monitor the switching process between Windows and the terminal. First you will want to view the keyswap service file to make sure you pass the correct arguments to xactive.sh. Most configurations do not really need the specific internal or usb id of your keyboard, but chromebook installs do require it.

```
cat ~/.config/systemd/user/keyswap.service
```

```
systemctl --user disable keyswap
systemctl --user stop keyswap

~/.config/xactive.sh mac 12 0 none
```

You can also refer to this Gist file to better understand what Kinto is doing and the simplicity of it. (The gist does not make use of any custom keymaps.)
https://gist.github.com/rbreaves/f4cf8a991eaeea893999964f5e83eebb

## Contributing

I welcome any and all contributors who want to contribute something to this project.

If you are specifically wanting to contribute additional custom keymaps to help with aligning Kinto's behavior to that of a mac keyboard then I would strongly recommend that you read Glen Whitney's comment on Superuser (the link is below). You may also look at the .xkb directory, mac_worsewise.sh and xactive.sh files to better understand how Kinto operates so that you can test your own keymaps without having to use the systemd service or running the xactive.sh script.

https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste

## More information about Kinto

https://medium.com/@benreaves/kinto-a-mac-inspired-keyboard-mapping-for-linux-58f731817c0

## License

GPL v2
