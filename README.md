# Kinto

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases/latest)

![alt text](https://github.com/rbreaves/kinto/blob/master/splash.png)

\- Type in Linux like it's a Mac. \-

Cmd = Ctrl+Shift for all terminals.

Note: As of version 1.0 Kinto no longer maps Cmd/Alt to Super while using the Terminal, it is now mapping to Ctrl+Shift by default. Please reset your terminal's keymaps back to their defaults.

Gnome-terminal reset
```
dconf reset -f /org/gnome/terminal/legacy/keybindings/
```

## What does this do exactly?

Kinto works for standard Windows, Apple and Chromebook keyboards. The following however describes the dynamic rebinding based on a standard Windows keyboard. (Alt location is Cmd for Apple keyboards)

- Normal apps - Alt will be Ctrl, Win/Super will be Alt, Ctrl will be Win/Super

- Terminal apps - Alt will be Ctrl+Shift, Win/Super will be Alt, Ctrl will be Ctrl

- Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

## What does Kinto require?

- Python (initial install only)
- systemd
- x11
- IBus*
- Debian/Ubuntu based distro 16.04+

If you need kintox11 recompiled for your distro please let me know and I will add a binary for your distro if my binary fails.

You can also attempt to compile kintox11.c on your system as well, but you will need to compile and install json-c first as its libraries will be required to compile and run the program.

*IBUS is needed to support wordwise during browser app usage as the keymap will need to change slightly depending if the cursor/caret is on screen waiting for input. You may install ibus with the following.

```
ibus-setup
im-config -n ibus
```
!! Please logoff and back on for IBus change to take effect!

To confirm navigate to your "Language Support" and set "Keyboard input method system:" to IBus for full word-wise support with web browsers.

Wayland support is planned, but not ready yet.

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
./setup.py
```

## JSON config files

Features
- Unlimited keyboard configurations per App/category (user_config.json - config -> create app object)
- Dynamic Desktop Environment shortcut capabilities (user_config.json - de -> create DE tweak/remap)

Located at ~/.config/kinto/ you will find user_config.json which will look like the following after an install. You can modify the defaults.json file in the root directory of kinto to create additional keyboard layout types/support without needing to modify any of the underlying Kinto code. 

You can also add additional Desktop Environment related tweaks to user_config.json in the install directory as well and the installer will prompt you to install them. You may also fork and submit any json or additional .xkb configurations to me for approval if you believe it makes Linux more like typing on a Mac.

```
{"config":[{
		"name":"gui",
		"run":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY",
		"de":[2],
		"appnames":[ "" ]
	},
	{
		"name":"term",
		"run":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.term $DISPLAY",
		"de":[2],
		"appnames":[ "Gnome-terminal","konsole","io.elementary.terminal","terminator","sakura","guake","tilda","xterm","eterm" ]
	}],
	"init": [1],
	"detypes":["gnome2","gnome3","kde4","kde5","xfce","i3wm"],
	"de":[{
		"id": 1,
		"type": ["gnome3"],
		"active": false,
		"intent":"init",
		"name":"gnome-init",
		"description":"Gnome - Remove Superkey Overlay keybinding to Activities Overview",
		"run":"gsettings set org.gnome.mutter overlay-key ''",
		"run_term":"",
		"run_gui":""
	},
	{
		"id": 2,
		"type": ["gnome3"],
		"active": false,
		"intent":"gui_term",
		"name":"Gnome Activities Overview",
		"description":"Cmd+Space activates Activities Overview",
		"run":"",
		"run_term":"gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Control><Shift>Space']\"",
		"run_gui":"gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Ctrl>Space']\""
	},
	{
		"id": 3,
		"type": ["kde5"],
		"active": false,
		"intent":"init",
		"name":"kde-init",
		"description":"KDE Plasma 5 - Removes Superkey Overlay from the Launcher Menu",
		"run":"kwriteconfig5 --file ~/.config/kwinrc --group ModifierOnlyShortcuts --key Meta \"\";qdbus org.kde.KWin /KWin reconfigure",
		"run_term":"",
		"run_gui":""
	}]
}
```

## How to Control Kinto

Under systemd this is how you control Kinto.

Status
```
systemctl --user status keyswap
```

Stop (and reset keyboard to normal)
```
systemctl --user stop keyswap && setxkbmap -option
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

### Does not start when you log in or after you reboot?

1. Check the status
```
systemctl --user status keyswap
```
2. Check the service journal
```
journalctl -xe
```

Open a ticket and send me the info.

### Keyswap is not occurring, but it was working.

Now that Kinto is using a custom written C program I am not aware of any specific bugs or issues, but you can start here if you having difficulties and please report it if it is reproducible.
1. Get status
```
systemctl --user status keyswap
```
2. Restart Kinto
```
systemctl --user restart keyswap
```
3. Check the Status again and open a ticket if you need to.
```
systemctl --user status keyswap
```

You can also do the following to see if it is an actual issue with kintox11 not running or your service file.
```
cd ~/.config/kinto
./kintox11
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

https://medium.com/@benreaves/kinto-v1-0-released-2018e6401d2e
https://medium.com/@benreaves/kinto-a-mac-inspired-keyboard-mapping-for-linux-58f731817c0

## License

GPL v2
