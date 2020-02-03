# Kinto

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases)

![alt text](https://github.com/rbreaves/kinto/blob/master/splash.png)

\- Type in Linux like it's a Mac. \-

Memory muscle matters for programmers and developers.

If it happens on your mac keyboard then it should happen the same in linux.

## What does this do exactly?

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/kinto-demo.gif)

Kinto works for standard Windows, Apple and Chromebook keyboards. The following however describes the dynamic rebinding based on a standard Windows keyboard.

- Normal apps - Alt will be Ctrl, Win/Super will be Alt, Ctrl will be Win/Super

- Terminal apps - Alt will be Ctrl+Shift, Win/Super will be Alt, Ctrl will be Ctrl

- Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

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

## Learning macOS style hotkeys on Linux

You can use websites like https://www.shortcutfoo.com in Google Chrome while using the terminal style keymap, but Firefox is not compatible due to detecting "cmd" as keycode 224. Chrome detects Win/Super/Cmd as keycode 91 on all OS's.

To make sure you are in the terminal style keymap you can just simply open the terminal and turn off the kinto service, and then switch back to Chrome.
```
systemctl --user stop keyswap && setxkbmap -option;setxkbmap -option altwin:swap_alt_win
```

## Troubleshooting

### Keyswap is not occurring, but it was working.

Now that Kinto is using a custom written C program I am not aware of any specific bugs or issues, but you can start here if you having difficulties and please report it if it is reproducible.

1. Restart Kinto
```
systemctl --user restart keyswap
```
2. Check the Status of Kinto and open a ticket with the output.
```
systemctl --user status keyswap
```

## Language Support
I'd appreciate any help from people with non-US based keyboards, to help ensure that these keymaps and keyswap methods work in all or most languages.

If you would like to attempt adding additional custom keymaps for other languages then I strongly recommend reading Glen Whitney's post here.
https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste

## Contributing

I welcome any and all contributors who want to contribute something to this project.

If you are specifically wanting to contribute additional custom keymaps to help with aligning Kinto's behavior to that of a mac keyboard then I would strongly recommend that you read Glen Whitney's comment on Superuser (the link is below). You may also look at the .xkb directory, mac_wordwise.sh and xactive.sh files to better understand how Kinto operates so that you can test your own keymaps without having to use the systemd service or running the xactive.sh script.

https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste

## More information about Kinto

https://medium.com/@benreaves/kinto-a-mac-inspired-keyboard-mapping-for-linux-58f731817c0

## License

GPL v2
