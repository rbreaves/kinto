# K!nt◎
[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases)

\- Fix the damn keyboard. -

Memory muscle matters for programmers and developers.

If it happens on your mac keyboard then it should happen the same in linux.

## What does this do exactly?

Remaps your keyboard to behave more like you're on a mac again and below is how the keymap will behave.

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
2. Install python3 (If needed)

Debian or Ubuntu 16.04 or 18.04
```
sudo apt update
sudo apt install python3
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

## Troubleshooting
If your keyboard is not being autodetected and configured then please run `xinput list`, if you are on linux, and copy the output into a ticket under issues.

## Known Issues

### USB Hubs

USB hubs may prevent Apple branded keyboards from loading properly or other Apple specific keyboards that are intended to make use of the "hid_apple" driver. Without this driver it is not possible to run the following command and have it swap alt and cmd.

```
echo '1' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd
```

This is required so that Apple and Windows keyboards can co-exist with the exact same keymappings, provided by setxkbmap. The solution for now is to avoid using a usb hub for your keyboard. Other possible solutions may be finding a way to patch the hid_apple module to accept other vendor and product id's so that it will still load the driver properly.

Other solutions may involve implementing a separate Mac system option in Kinto with a keyswap specific to a usb hub situation, however it will not be possible to have a Windows keyboard (aka internal laptop keyboard) working with the same keymap at the same time.

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

## Contributing

I welcome any and all contributors who want to contribute something to this project.

## License

GPL v2
