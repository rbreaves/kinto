# Kinto

![kinto_carrot](https://user-images.githubusercontent.com/10969616/77842401-4744b500-7157-11ea-854a-d7dec6f9a250.gif)

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases/latest)

\- Type in Linux & Windows like it's a Mac. \-

Seamless copy and paste with all apps and terminals. Also the only linux remapper that is aware of your cursor/caret status - meaning it avoids shortcut conflicts within an app versus wordwise shortcuts when a text field is in use.

## What does this do exactly?

Kinto works for standard Windows, Apple and Chromebook keyboards. The following however describes the dynamic rebinding based on a standard Windows keyboard. (Alt location is Cmd for Apple keyboards)

- Normal apps - Alt → Ctrl, Win/Super → Alt, Ctrl → Win/Super

- Terminal apps - Alt → Ctrl+Shift, Win/Super → Alt, Ctrl → Ctrl

- Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

## What does Kinto require?

- Python (initial install only)
- systemd
- x11
- IBus*
- Fedora/RHEL/Manjaro/Arch/Debian/Ubuntu based distro 16.04+
- xkeysnail (Recommended, but optional)

*IBus is needed to support wordwise during browser app usage as the keymap will need to change slightly depending if the cursor/caret is on screen waiting for input. Setup.py will set it but you can manually set it as well or check your current Input Method.

On most distros you can confirm navigate to your "Language Support" and set "Keyboard input method system:" to IBus for full word-wise support with web browsers. 

Wayland support is planned, but not ready yet.

## Kinto for Windows 10 Requirements

- WSL Ubuntu edition
- Powershell - run as Administrator
- Python3

Other programs that will be installed when you run ./setup.py
- Chocolatey
- Autohotkey

Does not have complete parity with the Linux edition, but it does work and can be built on and added to as needed. Modify ./windows/kinto.ahk if you want to add more WSL editions or other terminals.

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

To Uninstall Kinto

```
./setup.py
```

## Shortcut Creation (Xkeysnail)

**GUI Keys**
| Value| Description|Mac/Kinto Equivalent|
| ----- |:--------:|:--------:|
|C,Ctrl|Control|Cmd|
|M,Alt| Alt/Option|Alt/Option|
|Super | Win/Super|Ctrl|

**Terminal Keys**
| Value| Description|Mac/Kinto Equivalent|
| ----- |:--------:|:--------:|
|RC,RCtrl|Right Control on Left & Right Alt/Cmd key|Cmd|
|M,Alt| Alt/Option|Alt/Option|
|Ctrl | Ctrl|Ctrl|

You can define new keymaps for your specific app via this method. You also do not have to cancel out the original keybinding if you do not need or want to, but you can do so with "pass_through_key".

### Defining Keymaps Per App
```
# Keybindings for Sublime Text
define_keymap(re.compile("Sublime_text"),{
    K("C-h"): pass_through_key,          # cancel replace
    K("Ctrl-Alt-f"): K("Ctrl-h"),        # replace
    K("C-M-v"): [K("C-k"), K("C-v")],    # paste_from_history
}
```

In the above example I am also showing that you can define a single shortcut to enact multiple shortcut keys if needed by defining an array of shortcuts to trigger.

You can also make changes to the file in your /tmp/kinto/xkeysnail/kinto.py location and see them take affect in real time, but for your changes to be permanent you will need to make your changes in the ~/.config/kinto/kinto.py location & restart the xkeysnail service.

```
sudo systemctl restart xkeysnail
```

More information can be seen on the readme page of [xkeysnail](https://github.com/mooz/xkeysnail).

## Shortcut Creation (XKB)
The older xkb shortcut method info can be read about in ticket [#125](https://github.com/rbreaves/kinto/issues/125).

## Other Notes Related to Install

**Manjaro with Gnome there are issues.** 

Please see this ticket for more information.

https://github.com/rbreaves/kinto/issues/59

https://wiki.archlinux.org/index.php/IBus

**For other Arch based distros.**

Append the following and logoff and back on, but only after running setup.py to install all packages and the kinto service. Please report if there are any difficulties.
nano ~/.bashrc
```
export GTK_IM_MODULE=xim
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=xim
```

## How to Upgrade Kinto

Simply bring down the latest in either the master branch or dev, but dev is sometimes in flux as new features are being developed. Then you can re-run the setup.py installer, it will stop the service and re-install Kinto.

Note: If you have made any custom changes to ~/.xkb or ~/.config/kinto then you will need to backup or rename those directories before running an update.

```
git pull origin master
./setup.py
```

## How to Control Kinto

Under systemd this is how you control Kinto.

Kinto (xkb/x11) = keyswap

Kinto (udev/xkeysnail/x11) = xkeysnail

Status
```
systemctl --user status keyswap
sudo systemctl status xkeysnail
```

Stop (your keymap will return to normal)
```
systemctl --user stop keyswap
sudo systemctl stop xkeysnail
```

Start
```
systemctl --user start keyswap
sudo systemctl start xkeysnail
```

Restart
```
systemctl --user restart keyswap
sudo systemctl restart xkeysnail
```

Enable
```
systemctl --user enable keyswap
sudo systemctl enable xkeysnail
```

Disable
```
systemctl --user disable keyswap
sudo systemctl disable xkeysnail
```


## Learning macOS style hotkeys on Linux

You can use websites like https://www.shortcutfoo.com in Google Chrome while using the terminal style keymap, but Firefox is not compatible due to detecting "cmd" as keycode 224. Chrome detects Win/Super/Cmd as keycode 91 on all OS's.

To make sure you are in the terminal style keymap you can just simply open the terminal and turn off the kinto service, and then switch back to Chrome.
```
systemctl --user stop keyswap && setxkbmap -option;setxkbmap -option altwin:swap_alt_win
```

## Troubleshooting

### Does not start when you log in or after you reboot?

Kinto (xkb/x11) = keyswap

Kinto (udev/xkeysnail/x11) = xkeysnail

1. Check the status
```
systemctl --user status keyswap
sudo systemctl status xkeysnail
```
2. Check the service journal
```
journalctl --user-unit=keyswap.service -b
sudo journalctl --unit=xkeysnail.service -b
```

Note: You can also watch your log live
```
journalctl -l --user-unit=keyswap.service -b
sudo journalctl -l --unit=xkeysnail.service -b
```

You may need to manually set your DISPLAY in the systemd service file. Normally it pulls in the proper DISPLAY value but if it doesn't you can try this.

```
echo $DISPLAY

# :0.0
```

nano ~/.config/systemd/user/keyswap.service

sudo nano /etc/systemd/system/xkeysnail.service
```
...
[Service]
Type=simple
Restart=always
Environment=DISPLAY=:0.0
...
```

If you continue to have issues then open a ticket and send me the info.

### Keyswap is not occurring, but it was working.

Kinto (xkb/x11) = keyswap

Kinto (udev/xkeysnail/x11) = xkeysnail

Now that Kinto (xkb/x11) is using a custom written C program I am not aware of any specific bugs or issues, but you can start here if you having difficulties and please report it if it is reproducible.

1. Get status
```
systemctl --user status keyswap
sudo systemctl status xkeysnail
```
2. Restart Kinto
```
systemctl --user restart keyswap
sudo systemctl restart xkeysnail
```
3. Check the Status again and open a ticket if you need to.
```
systemctl --user status keyswap
sudo systemctl status xkeysnail
```

You can also do the following to see if it is an actual issue with kintox11 not running or your service file.
```
cd ~/.config/kinto
./kintox11
```

## Debug

If all else fails you can now run Kinto in debug mode as of 1.0.6-2. The output will become more verbose and I'd recommend running this directly after stopping the service.

Kinto (xkb/x11)
```
systemctl --user stop keyswap
cd ~/.config/kinto
./kintox11 --debug
```

Kinto (udev/xkeysnail)

Stop
```
sudo systemctl stop xkeysnail
```
nano ~/.config/kinto/xkeystart.sh

Remove the 2 instances of --quiet and resave
```
#!/bin/bash

/usr/local/bin/xkeysnail --quiet --watch "$1" &

inotifywait -m -e close_write,moved_to,create -q "$1" |
while read -r path; do
        /usr/bin/killall xkeysnail
        /usr/local/bin/xkeysnail --quiet --watch "$1" &
done
```
Start
```
sudo systemctl start xkeysnail
sudo systemctl status xkeysnail
```

## Language Support
I'd appreciate any help from people with non-US based keyboards, to help ensure that these keymaps and keyswap methods work in all or most languages.

If you would like to attempt adding additional custom keymaps for other languages then I strongly recommend reading Glen Whitney's post here.
https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste

## Notes about Windows 10
Sharpkeys was used to create the layout/reg files to swap the Ctrl, Win and Alt keys. Sharpkeys was not required however because the reg keys were extracted. Autohotkey is used to manage keyswaps needed for terminal usage. Autohotkey is also used to add additional mac like keybinds for Sublime text and can be used for other apps as well.

Microsoft is working on a new Powertoy Keyboard Manager that could be used with an easier to use GUI interface, but this approach should be fully sufficient for a mac like experience and autohotkeys appears to be more than capable enough to handle complex rebinding of any or most mac like shortcuts.

## Contributing

I welcome any and all contributors who want to contribute something to this project.

If you are specifically wanting to contribute additional custom keymaps to help with aligning Kinto's behavior to that of a mac keyboard then I would strongly recommend that you read Glen Whitney's comment on Superuser (the link is below). You may also look at the .xkb directory, mac_wordwise.sh and xactive.sh files to better understand how Kinto operates so that you can test your own keymaps without having to use the systemd service or running the xactive.sh script.

https://superuser.com/questions/385748/binding-superc-superv-to-copy-and-paste

## More information about Kinto

https://medium.com/@benreaves/kinto-v1-0-released-2018e6401d2e
https://medium.com/@benreaves/kinto-a-mac-inspired-keyboard-mapping-for-linux-58f731817c0

## License

GPL v2

## Credits and Contributions

I would just like to thank a few people here directly that have helped me tremendously with completing this project and without their support, direct, indirect or otherwise I would have had difficulty completing this undertaking. I will list these things off in chronological order mostly.

First off I'd like to thank the Stackoverflow and Stackexchange community. I have probably rubbed some mods the wrong way over there, but the people from the community in general are extremely helpful and gracious and without their contributions would have made this much more difficult. The person I'd like to thank most though from over there is Glen Whitney. Without his detailed explaining of how to rebind keys in xkb this would not have come together at all, as every other remapping solution were non-starters as complexity increases.

Secondarily I'd like to thank Christian Eriksson*, as he provided information that kept me up at night.. literally. Even after I implemented a similar bash script to one he had suggested I knew that fully implementing a c/c++ solution was where Kinto needed to head to and his explaination was better than I remember it being now that I have gone back to read it again. He also never provided a full implementation of a c/c++ solution - he did hit on the pain points pretty well of what one would need to do and watch out for. I am not sure where I got the first example code of implementing a c based solution, but he definitely went over it well.


Kui and his gist file** was really the c based solution that I found had the fewest issues to resolve to making it a reliable solution. It didn't account for all failures very well, aka BadWindow issues, but it made for a great foundation on which Kintox11 is built. I cannot thank him enough for putting it out there for others to work with.

Lastly these four people were also very helpful to me as well. @probonopd for being one of the first people to install and use Kinto and gave me the initial feedback to include wordwise support! He also has really great articles*** posted on HackerNews & Medium about UI/UX design. Another person I'd like to thank is @owzim, his feedback allowed me to rapidly iterate and fix several bugs to support additional platforms better. The last two are members of the #ubuntu channel in IRC on freenode, tarzeau ( @alexmyczko ) and sarnold. Alex contributing a proper Makefile, so the project can be packaged properly, and sarnold help me find that IBus could resolve an issue I was having with needing to detect the caret status.

If I left anyone out then I apologize, that was not intentional. I am happy to say that this project is at a state of completion. Bug fixes will primarily be the only activity happening going forward and possibly a rewrite for Wayland at some point. Contributions as mentioned above are welcomed, and will be merged into master if they help with the goal of making typing on linux more like a mac.

*https://askubuntu.com/questions/1010276/can-i-act-on-the-event-that-a-window-opens-without-polling

**https://gist.github.com/kui/2622504

***https://medium.com/@probonopd/make-it-simple-linux-desktop-usability-part-1-5fa0fb369b42
