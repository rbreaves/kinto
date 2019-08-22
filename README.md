# Kinto

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases)

\- A better linux keyboard layout for professional mac users \-

Memory muscle matters for programmers and developers.

If it happens on your mac keyboard then it should happen the same in linux.

## What does this do exactly?

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/kinto-demo.gif)

Kinto works for standard Windows, Apple and Chromebook keyboards. The following however describes the dynamic rebinding based on a standard Windows keyboard.

- Normal apps - Alt will be Ctrl, Win/Super will be Alt, Ctrl will be Win/Super

- Terminal apps (optional) - Alt will be Win/Super, Win/Super will be Alt, Ctrl will be Ctrl

- New Features - Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

## What does Kinto require?

- Python (initial install only)
- systemd
- x11

Wayland support is planned, but not ready yet.

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

Restart
```
systemctl --user restart keyswap
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

I have not automated this part of the install due to the wide range of DE's and each one needing the shortcut setup to be a little different.

Here's what you will want to do, if you want to set this up.

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
4. Go into the DE system settings and bind the hotkeys you want to use to activate it.


## Learning macOS style hotkeys on Linux

You can use websites like https://www.shortcutfoo.com in Google Chrome while using the terminal style keymap, but Firefox is not compatible due to detecting "cmd" as keycode 224. Chrome detects Win/Super/Cmd as keycode 91 on all OS's.

To make sure you are in the terminal style keymap you can just simply open the terminal and turn off the kinto service, and then switch back to Chrome.
```
systemctl --user stop keyswap
```

or alternatively, you can follow the instructions about how to manually trigger a toggle of the keyswap.

## Troubleshooting

### Keyswap is not occurring, but it was working.
Sometimes something about the Desktop Environment may throw xprop for a loop, it's rare, but if this occurs then you have 2 options.
1. Restart Kinto
```
systemctl --user restart keyswap
```
2. Check the Status of Kinto and open a ticket with the output, especially if you can reliably reproduce the problem.
```
systemctl --user status keyswap
```

### Chromebook with external keyboard not being detected
If your keyboard is not being autodetected and configured then please run `xinput list`, if you are on linux, and copy the output into a ticket under issues.

## Language Support
I'd appreciate any help from people with non-US based keyboards, to help ensure that these keymaps and keyswap methods work in all or most languages.

If you would like to attempt adding additional custom keymaps for other languages then I strongly recommend reading Glen Whitney's post here.
https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste


## Known Issues

### USB Hubs

No longer an issue. USB hubs may prevent Apple keyboards from loading an official driver, but Kinto will adapt if this occurs. The benefit of an official Apple driver is that it can allow Kinto to support a mix of Windows and Mac based keyboards simultaneously.

## Debugging

You can output the xactive.sh script with parameters with following command.

```
cat ~/.config/systemd/user/keyswap.service
```

After that just stop the service as described and run the xactive.sh script with parameters.

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
