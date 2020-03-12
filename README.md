# Kinto

![alt text](https://raw.githubusercontent.com/rbreaves/kinto/master/Kinto.png)

[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases/latest)

![alt text](https://github.com/rbreaves/kinto/blob/master/splash.png)

\- Type in Linux like it's a Mac. \-

Seamless copy and paste with all apps and terminals. Also the only linux remapper that is aware of your cursor/caret status - meaning it avoids shortcut conflicts within an app versus wordwise shortcuts when a text field is in use.

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
- Fedora/RHEL/Manjaro/Arch/Debian/Ubuntu based distro 16.04+

If you need kintox11 recompiled for your distro please let me know and I will add a binary for your distro if my binary fails.

You can also attempt to compile kintox11.c on your system as well, but you will need to compile and install json-c first as its libraries will be required to compile and run the program.

*IBus is needed to support wordwise during browser app usage as the keymap will need to change slightly depending if the cursor/caret is on screen waiting for input. Setup.py will set it but you can manually set it as well or check your current Input Method.

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

To Uninstall Kinto

```
./uninstall.sh
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

Status
```
systemctl --user status keyswap
```

Stop (your keymap will return to normal)
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

## How to Add Setxkbmap Option inside Kinto

To summarize you'll need to pull the partial out of the symbols file the option resides in and then add that to the mac_gui file and lastly reference it in the keymap file(s) you want it in.

symbols directory
```
/usr/share/X11/xkb/symbols/ 
```

symbols file
```
~/.xkb/symbols/mac_gui
```

keymap files
```
~/.xkb/keymap/kbd.mac.gui
~/.xkb/keymap/kbd.mac.term
```

A more detailed explaination is here.
https://github.com/rbreaves/kinto/issues/50#issuecomment-595953373

## How to Add or Change keymaps for Applications

Note: All of the following is already done in Kinto (but may also change as improvements are made). The following is purely for documentation and example sake as they are real examples of how to leverage the json config to support additional keymaps.

**First it is important to understand how Kinto operates.**

1. It listens for any focus/active window changes
2. It applies the proper keymap based on the programs name.
3. It may monitor your caret/cursor input status, if the app is known to cause shortcut conflicts with wordwise
4. It runs anywhere from 1 to 3 commands to fully remap your computer.

Ok great, we've covered the basics, now what are your options on modifying functionality?
It depends.

Do you want to remap keys using xkb or xbindkeys with xdotool, or something else entirely?
The choice is yours, but I'd recommend xbindkeys with xdotool for anyone that doesn't want to spend the time or learn xkb. I prefer xkb but it completely remaps your keyboard and it could break things if done poorly.

**How to Remap using XBindKeys with Xdotool - Firefox**

1. By default Firefox is mapped with the standard gui based xkb config, and only if no input has focus does it then run xbindkeys to map the Cmd+Left/Right arrow key location to the Back and Forwards functionality you'd expect.

2. The xbindkeys script takes into account the xkb mapping being the base because it is actually remapping Home and End to Back and Forwards as there is no real reason to reload an entire xkb layout.

~/.config/kinto/user_config.json
```
...
{
    "name": "firefox",
    "run": "setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY",
    "run_onInput": "killall xbindkeys > /dev/null 2>&1",
    "run_offInput": "killall xbindkeys > /dev/null 2>&1;xbindkeys -f $HOME/.config/kinto/.firefox-nw",
    "symbols": "",
    "types": "",
    "de": [
	2
    ],
    "appnames": [
	"Firefox"
    ]
},
...
```
~/.config/kinto/.firefox-nw
```
"xdotool key --delay 0 --clearmodifiers Control_L+bracketleft"
  // Alt/Cmd + Left
  Home + Release

"xdotool key --delay 0 --clearmodifiers Control_L+bracketright"
  // Alt/Cmd + Right
  End + Release
  
# Note additional keymaps can easily be added to this file and I will accept any PR's with keymaps that align with macs
```

Once you have made your changes you can restart the Kinto service and the changes will take affect.
```
systemctl --user restart keyswap
```

Under normal circumstances this keymap would not have worked well had Firefox not included 2 keymap options for going forwards or back. In the next example, Chrome, you will see how to solve this very same problem but in xkb format and it is the only way to fix it for Chrome due to conflicting with wordwise shortcuts.

Also the choice of xdotool over something like xte (xautomation) was explicit, xdotool allows you to hold down a modifier and continue to repeat the action(s) and xte does not.

**How to Remap Using XKB - Chrome**

This gets to be a little more complicated, but this is what you have to do to accomplish the same on the xkb level.

**Summary**
1. Copy ~/.xkb/keymap/kbd.mac.gui and append the name of the app. (e.g. chrome)
2. Edit ~/.xkb/keymap/kbd.mac.gui.chrome
3. Add new keybindings to ~/.xkb/symbols/mac_gui
4. Only edit types if you absolutely need to add another modifier level (~/.xkb/types/mac_gui)

Understand that as you add or modify the ~/.xkb/symbols/ files that these two groups **symbols[Group1]** and **actions[Group1]** will be following the order of the modifier levels that are configured in the related ~/.xkb/types/mac_gui or mac_term file.

Also you will have to discover the proper xkb names for keys and that they will often follow *two different* labels/names. eg RGHT vs Right ... **replace key \<RGHT\>** vs **symbols[Group1]= [ Right, ...**.

A good place to get the proper names/labels are these two files.
```
/usr/share/X11/xkb/symbols/us
/usr/share/X11/xkb/symbols/inet
```

Ok, so here are the detailed instructions.

1. cp ~/.xkb/keymap/kbd.mac.gui ~/.xkb/keymap/kbd.mac.gui.chrome

2. nano ~/.xkb/keymap/kbd.mac.gui.chrome
```
# Change mac_gui(mac_levelssym)
...
xkb_symbols   { include "pc+us+us:2+inet(evdev)+ctrl(swap_lwin_lctl)+ctrl(swap_rwin_rctl)+mac_gui(mac_levelssym)"	};
...
# To +mac_gui(mac_chrome)
xkb_symbols   { include "pc+us+us:2+inet(evdev)+ctrl(swap_lwin_lctl)+ctrl(swap_rwin_rctl)+mac_gui(mac_chrome)"	};
...
};
```

3. Add your new "partial xkb_symbols" via nano ~/.xkb/symbols/mac_gui
```
partial xkb_symbols "mac_chrome" {
    // Back Button
    replace key <LEFT> {
        type[Group1]= "ONE_LEVEL_CTRL",
        symbols[Group1]= [
            Left,
            Left,
            Left
        ],
        actions[Group1]= [
            NoAction(),
            RedirectKey(key=<UP>),
            RedirectKey(key=<LEFT>,modifiers=Mod1,clearmods=Control)
        ]
    };
    // Forwards Button
    replace key <RGHT> {
        type[Group1]= "ONE_LEVEL_CTRL",
        symbols[Group1]= [
            Right,
            Right,
            Right
        ],
        actions[Group1]= [
            NoAction(),
            RedirectKey(key=<DOWN>),
            RedirectKey(key=<RGHT>,modifiers=Mod1,clearmods=Control)
        ]
    };
```

~/.config/kinto/user_config.json
```
{
    "name": "chrome",
    "run": "setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui.chrome $DISPLAY",
    "run_onInput": "xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY",
    "run_offInput": "xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui.chrome $DISPLAY",
    "symbols": "",
    "types": "",
    "de": [
	2
    ],
    "appnames": [
	"Chromium",
	"Chromium-browser",
	"Google-chrome"
    ]
}
```
4. Not making changes to types but it looks like this. It contains 5 levels of modifiers, Base, Alt, Control, Shift+Control, and Shift+Alt. Additional Levels can and may be added later, but please do not change the order of the Levels or existing symbols files will break!! You can add new levels however without issue.
```
default partial xkb_types "addmac_levels" {
    type "ONE_LEVEL_CTRL" {
        modifiers= Mod1+Control+Shift;
        map[Mod1]= Level2;
        map[Control]= Level3;
        map[Mod1+Control]= Level3;
        map[Shift+Control]= Level4;
        map[Shift+Mod1] = Level5;
        level_name[Level1]= "Base";
        level_name[Level2]= "Alt";
        level_name[Level3]= "Control";
        level_name[Level4]= "Shift with Control";
        level_name[Level5] = "Shift Alt";
    };
};
```

Once you have made your changes you can restart the Kinto service and the changes will take affect.
```
systemctl --user restart keyswap
```

## JSON config files

Features
- Unlimited keyboard configurations per App/category (user_config.json - config -> create app object)
- Dynamic Desktop Environment shortcut capabilities (user_config.json - de -> create DE tweak/remap)

Located at ~/.config/kinto/ you will find user_config.json which will look like the following after an install. You can modify the defaults.json file in the root directory of kinto to create additional keyboard layout types/support without needing to modify any of the underlying Kinto code. 

You can also add additional Desktop Environment related tweaks to user_config.json in the install directory as well and the installer will prompt you to install them. You may also fork and submit any json or additional .xkb configurations to me for approval if you believe it makes Linux more like typing on a Mac.

```
{"config":[
	//
	// Each config category contains the category name, and references to the de tweaks
	// And contains the default run commands plus what behavior they should exhibit for
	// input fields on/off focus, if any.
	// Symbols and types are not currently used - may later replace the need for static
	// files with xkbcomp.
	//
	// If you use xbindkeys outside of Kinto then you may want to remove xbindkeys from
	// this config after setup or rewrite the command to exclude your own xbindkeys.
	//
	{
		"name":"gui",
		"run":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY",
		"de":[2],
		"appnames":[ "" ],
		"run_onInput":"",
		"run_offInput": "killall xbindkeys > /dev/null 2>&1",
		"symbols":"",
		"types":"",
		"de":[],
		"appnames":[ "" ]
	},
	{
		"name":"term",
		"run":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.term $DISPLAY",
		"de":[2],
		"appnames":[ "Gnome-terminal","konsole","io.elementary.terminal","terminator","sakura","guake","tilda","xterm","eterm" ],
		"run_onInput":"",
		"run_offInput": "killall xbindkeys > /dev/null 2>&1",
		"symbols":"",
		"types":"",
		"de":[],
		"appnames":[ "" ]
	}],
	// Init - Array that references de objects by their ID and runs the "run" command
	// when the app initially runs.
	"init": [1],
	// detypes - DE's with support or planned support
	"detypes":["gnome2","gnome3","kde4","kde5","xfce","i3wm"],
	// de - tweak objects and initial command to be ran on start.
	//
	//    Intent - init or gui_term, to signify what type of tweak it is.
	//      run, run_term, run_gui - run is only relevant for init, and the
	//      other two relate to gui_term and running under those modes.
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
journalctl --user-unit=keyswap.service -b
```

You may need to manually set your DISPLAY in the systemd service file. Normally it pulls in the proper DISPLAY value but if it doesn't you can try this.

```
echo $DISPLAY

# :0.0
```

nano ~/.config/systemd/user/keyswap.service
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
