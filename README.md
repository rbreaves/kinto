# Kinto.sh

![kinto-color-132](https://user-images.githubusercontent.com/10969616/94909977-9d2d4900-0469-11eb-8710-986289fe7240.gif)


[![GitHub release](https://img.shields.io/github/release/rbreaves/kinto.svg)](https://github.com/rbreaves/kinto/releases/latest)

\- Mac-style shortcut keys for Linux & Windows. \-

Seamless copy and paste with all apps and terminals. The zero effort solution.

v1.2 Release - Kinto now includes a system tray and simple wizard to setup the install with minimal effort.

Kinto is powered by [xkeysnail](https://github.com/mooz/xkeysnail) for Linux & by [Autohotkey](https://github.com/Lexikos/AutoHotkey_L) for Windows 10.

### [Table of Contents ](#Table-of-Contents)

## Donations

If you like or appreciate this project then please consider donating.

|**Wishlists**|[Amazon](https://smile.amazon.com/hz/wishlist/ls/3EVXR21VFKD9Z?ref_=wl_share)|[Adafruit](https://www.adafruit.com/wishlists/515932)|[eBay](https://www.ebay.com/mye/myebay/WatchList?custom_list_id=636668138019)|
|---|---|---|---|

If you would like to send me a keyboard directly then please reach out to me over [twitter](https://twitter.com/gbit86) and send me a DM.

## How to install (Linux)

Video Tutorial: [Install Kinto.sh for Linux in less than a minute](https://www.youtube.com/watch?v=kd4al45XD1g)

[Linux Requirements](#What-does-Kinto-require)

<img src="https://user-images.githubusercontent.com/10969616/97070698-179c4500-15a0-11eb-8064-c03aa7f4d4a5.png" width="75%">

### Quick Install Method

Paste the following into your Terminal
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rbreaves/kinto/HEAD/install/linux.sh)"
```

Uninstall
```
/bin/bash <( curl https://raw.githubusercontent.com/rbreaves/kinto/HEAD/install/linux.sh ) -r
```

### Old Install Method

```
git clone https://github.com/rbreaves/kinto.git
cd kinto
sudo apt update
sudo apt install python3
./setup.py
```

**Troubleshoot**

If the wizard does not appear then either type in "kinto.sh" in your application overview search bar or run this following command.
```
~/.config/kinto/gui/kinto-gui.py
```

**Issues with Numpad?**

Try toggling numlock on & off (clear key on official mac keyboards). If it still does not work then restart the Kinto service and try toggling the numlock/clear key again, it will likely work after that. #369

**Uninstall Kinto**

```
./setup.py -r
```

**Other tips**

If you want a global menu app similar to what mac users have then I strongly recommend Ubuntu Budgie as it has the Vala Appmenu built in and ready for activation. Short of that Vala-AppMenu can be installed in various distros, mileage will vary. If you try to activate it in the latest 20.xx releases with XFCE then you may need to run the following commands.

```
sudo apt install xfce4-appmenu-plugin vala-panel-appmenu-common
xfconf-query -c xsettings -p /Gtk/Modules -n -t string -s "appmenu-gtk-module"
```

**Perfect HiDPI fractional scaling on Ubuntu Budgie 20.04 under x11**

https://discourse.ubuntubudgie.org/t/ubuntu-budgie-20-04-fractional-hidpi-for-x11/4777

## How to Install (Windows)

Video Tutorial: [How to Install Kinto.sh on Windows 10](https://youtu.be/sRk8A8krz40)

[Windows 10 Requirements](#Kinto-for-Windows-10-Requirements)

### Quick install
Open Powershell as Administrator and copy and paste the following. This will download & extract Kinto, install chocolatey, python3 and then install Kinto.

**⚠ NOTE: Please inspect https://raw.githubusercontent.com/rbreaves/kinto/master/install/windows.ps1 and https://chocolatey.org/install.ps1 before running scripts directly. More information about running powershell scripts in this context can be found [here](https://chocolatey.org/install).**

```
Set-ExecutionPolicy Bypass -Scope Process -Force
iwr https://raw.githubusercontent.com/rbreaves/kinto/master/install/windows.ps1 -UseBasicParsing | iex
```


Update system tray to show Kinto icon at all times (optional)
```
cmd /c "explorer shell:::{05d7b0f4-2121-4eff-bf6b-ed3f69b894d9}"
```

### Old method

1. Open Powershell (Right click and Run as Administrator)

2. clone this repo
```
git clone https://github.com/rbreaves/kinto.git
cd kinto
```
3. Install - Select keyboard type
```
py setup.py
```

4. How to make Kinto stay visible in system tray (optional)

<img src="https://user-images.githubusercontent.com/10969616/85195077-2f338c00-b295-11ea-8aa3-e6aa06a9a279.png" width="50%" height="50%">
<img src="https://user-images.githubusercontent.com/10969616/85195079-30fd4f80-b295-11ea-8bcd-257990b77dcb.png" width="50%" height="50%">
<img src="https://user-images.githubusercontent.com/10969616/85195082-322e7c80-b295-11ea-8c81-320dab424c3c.png" width="50%" height="50%">

**Uninstall Kinto**

```
py setup.py
```

Select Uninstall

## How to use in Remote Desktop Solutions

RDP fully works as long as the entire keyboard input is being captured. RDP had been working for awhile with Windows but as of 2/14/2021 Linux & macOS is now supported. VNC & other protocols may work, but is likely most dependent on how the keyboard input is captured on the computer running the client.

|Program|Src/Remote Client ⇒|Dst/Remote Server|Works? |Notes|
|---|---|---|---|---|
|Official MS RDP (mstsc.exe)| ❖Windows ⇒| ❖Windows  | ✅ Yes|   |
|Official MS RDP| ChromeOS 87+⇒| ❖Windows  | ✅ Yes|May work on earlier versions as well, if they support Android apps|
|Remmina| 🐧Linux*/ChromeOS 87+⇒| ❖Windows  | ✅ Yes|*Use hover menu to enable "Grab all keyboard events"|
|FreeRDP| 🐧Linux/ChromeOS 87+⇒| ❖Windows  | ✅ Yes | |
|FreeRDP| 🍎macOS⇒| ❖Windows  | ✅ Yes| [FreeRDP for macOS](#FreeRDP-for-macOS)|
|Remote Desktop Manager Free|🍎iOS⇒| ❖Windows  | ✅ Yes| |
|Jump Desktop (RDP)| 🍎macOS*/iOS ⇒| ❖Windows  | ✅ Yes|*Preferences -> Keyboard -> Disable "Key Conversions", Enabled "Send macOS Shortcuts" under Keyboard shortcuts|
|Official MS RDP| 🍎macOS⇒| ❖Windows  | ❌ No|Initial Cmd key press not being passed|
|Remote Desktop Manager Free| 🍎macOS⇒| ❖Windows  | ❌ No|Initial Cmd key press not being passed|
|Royal TSX Client| 🍎macOS⇒| ❖Windows  | ❌ No|Initial Cmd key press not being passed|
|Official MS RDP| 🍎🤖iOS/Android⇒| ❖Windows  | ❌ No|No workaround atm|

## FreeRDP for macOS

1. Install [brew.sh](https://brew.sh).

```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```

2. Install XQuartz (x11/xorg)

```brew install --cask xquartz```

3. log off and back on.
4. Install FreeRDP

```brew install freerdp```

5. Disable [NLA](https://kb.parallels.com/en/123661), if it is enabled on the destination.
6. Run command to access machine
Note: 192.168.x.x = Your IP.

```xfreerdp /u:your_username /v:192.168.x.x /cert-ignore /auto-reconnect-max-retries:0 /f +clipboard -decorations```

7. Click on XQuartz -> Preferences and set these checkmarks so that fullscreen can work, may need to quit it and re-run the xfreerdp command from step 6.

<img src="https://user-images.githubusercontent.com/10969616/108144025-68bfcf80-708e-11eb-96cc-2930b7b1694a.png" width="50%">

More info here
https://medium.com/idomongodb/macos-rdp-to-a-windows-machine-1e0f52f777b

## Jump Desktop for macOS

Screenshots of how to configure Jump Desktop for macOS users accessing a Windows PC with Kinto installed. I apologize that it is not a free RDP client - BUT it does work, and at $15 it is reasonable if you plan to use it frequently.

<img src="https://user-images.githubusercontent.com/10969616/107990246-a2fb7500-6f99-11eb-8c19-0a9b538b996f.png" width="25%">
<img src="https://user-images.githubusercontent.com/10969616/107990265-a8f15600-6f99-11eb-9922-bbcfa0b92031.png" width="50%">
<img src="https://user-images.githubusercontent.com/10969616/107990256-a68efc00-6f99-11eb-9f31-575ed6016944.png" width="50%">


## Table of Contents

[How to install (Linux)](#How-to-install-Linux)

[How to install (Windows)](#How-to-install-Windows)

[What does this do exactly?](#What-does-this-do-exactly)

[What's different from other remappers?](#Whats-different)

[What does Kinto require?](#What-does-Kinto-require)

[Shortcut Creation](#Shortcut-Creation)

[How to Upgrade/Control Kinto](#How-to-Upgrade-Kinto)

[Troubleshooting](#Troubleshooting)

[Language Support](#Language-Support)

[Related or Useful Resources](#Related-or-Useful-Resources)

[Contributing](#Contributing)

[More information about Kinto](#More-information-about-Kinto)

[License](#License)

[Credits and Contributions](#Credits-and-Contributions)

## What does this do exactly?

Kinto works for standard Windows, Apple and Chromebook keyboards. The following however describes the dynamic rebinding based on a standard Windows/Mac keyboard.

- Cursor/word-wise shortcut keys have been added to align with macOS keyboard shortcuts.

**GUI**
|**Physical**| Ctrl  |  Win/Alt |  Alt/Cmd | Spacebar|
|---|---|---|---|---|
|**Virtual**|  Win/Super* | Alt  |  RCtrl |Spacebar|

*Win/Super will properly remap to LCtrl when needed to fully support expected keymaps.

**Terminal**
|**Physical**| Ctrl  |  Win/Alt |  Alt/Cmd | Spacebar|
|---|---|---|---|---|
|**Virtual**|  LCtrl | Alt  |  RCtrl |Spacebar|

Note: RCtrl for terminals is also adding in Shift most of the time, however it depends on the specific terminal in use and will change itself to the expected keymaps of that terminal application.

## What's different?

Compared to most other remappers ***this is a complete system-wide remap of your base level modifier keys***, this saves time. You're not going to die a death of a thousand papercuts from trying to support every shortcut key under the sun.

It also retains some of the most commonly used system level shortcut keys, such as Cmd-C/V, Cmd-Tab, and Ctrl-Tab among others. You will keep seamless copy & paste between all apps, ability to switch Windows while still using the physical Cmd/Alt key position; switch tabs in your favorite terminals, code editors, or web browsers. Depending on your OS and/or Desktop Environment you may also be able to switch Virtual Desktop environments the same way as well and other basic system level shortcuts.

If your OS and macOS have similar functionality on the system level, but only differ by a slight difference of a shortcut command then Kinto likely supports it already. If Kinto doesn't have what you need then you can open up a support ticket and it will be added. You can also fork the project to add the fix and I will merge it via a PR you make.

Additionally, if you are using a cross-platform app and if it happens to have a few shortcut keys that differ then that can very easily be added to either the kinto.py or kinto.ahk configuration files which on Windows is located here `~/.kinto/kinto.ahk` and on Linux it can be found here `~/.config/kinto/kinto.py`. More info can be found here [Shortcut Creation](#Shortcut-Creation)

## What does Kinto require?

- Python
- systemd
- x11
- xkeysnail

### Kinto for Windows 10 Requirements

- [Git for Windows](https://git-scm.com/download/win)
- Powershell - run as Administrator
- [Python3](https://www.python.org/downloads/windows/)

Other programs that will be installed when you run ./setup.py
- Chocolatey
- Autohotkey
- Strawberry Perl

Note: Sublime Text users should disable screen rotation hotkeys as they will interfere with multi-cursor and possibly other combos. See https://windowsloop.com/disable-screen-rotation-keyboard-shortcut/ for details.

You may also want to disable the Xbox Game Bar so that Win+G or other shortcuts will not interfer with any of your remaps. Start menu -> Game bar shortcuts -> toggle Off.

## Shortcut Creation

[Linux Shortcut Creation (Xkeysnail)](#Linux-Xkeysnail)

[Windows Shortcut Creation (Autohotkey)](#Windows-Autohotkey)


## Linux (Xkeysnail)

**GUI Keys**
| Value| Description|Mac/Kinto Equivalent|
| ----- |:--------:|:--------:|
|C,Ctrl|Control|Cmd|
|M,Alt| Alt/Option|Alt/Option|
|Super | Win/Super|Ctrl|

**Terminal Keys**
| Value| Description|Mac/Kinto Equivalent|
| ----- |:--------:|:--------:|
|RC,RCtrl|Right Control → Left & Right Alt/Cmd key|Cmd|
|M,Alt|Alt/Option|Alt/Option|
|LC,LCtrl |Left Control|Ctrl|

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

## Windows (Autohotkey)

This applies to the Windows version of Kinto and how to add additional support for Applications. The configuration file location is `~/.kinto/kinto.ahk` and after updating it you will want to right click on the tray icon and click on setting your keyboard type again and it will re-apply the latest changes.

Windows 10 has a couple of ways that you need to be aware of when trying to add a specific application, the typical method of how to add any exe program, but then there is also the newer UWP app format that some applications use which will require a similar but different method, both will be discussed.

### Defining Keymaps Per App by EXE Name
You can use the following legend **but** realize that these remaps reference the Virtual keys in the diagrams mentioned near the beginning of this document, so **do not** confuse it with the physical key unless they happen to be the same key.

|Autohotkey Symbol|Virtual key|Description|
|---|---|---|
|^,Ctrl|Control|Primary modifier, 1st rock from the spacebar|
|!,Alt|Alt|Secondary modifier, 2nd rock from the spacebar|
|#,Win|Win/Super|Tertiary modifier, 3rd rock from the spacebar|

```
...
#IfWinActive ahk_exe sublime_text.exe
    #^Up::send !{O}                                         ; Switch file
    #^f::send {F11}                                         ; toggle_full_screen
    ^!v::send {Ctrl Down}k{Ctrl Up}{Ctrl Down}v{Ctrl Up}    ; paste_from_history
    ...
#If
...
```

With this being Autohotkey you can easily pull knowledge from the Autohotkey forums for just about any issue you may have as well.

### Defining Keymaps Per UWP App

```
#If WinActive("- OneNote ahk_class ApplicationFrameWindow", "OneNote")
...
    ; Add your keymaps here
...
#If
```

I don't have too many examples on this one, most developers seem to be shying away from UWP. Kinto currently supports "Fluent Terminal" which is a UWP app, but it is also being grouped with other Terminal apps for hotkey remapping. You may take a look at that, but you may also want to try creating a new Autohotkey file and use the Window Spy feature built into Autohotkey to help you discover the full name and class names of any application.

## Shortcut Creation (XKB)
The older xkb shortcut method info can be read about in ticket [#125](https://github.com/rbreaves/kinto/issues/125).

## How to Upgrade Kinto

Simply bring down the latest then you can re-run the setup.py installer, it will stop the service and re-install Kinto.

Note: If you have made any custom changes to ~/.config/kinto then you will need to backup or rename those directories before running an update.

```
git pull origin master
./setup.py
```

## How to Control Kinto

This info is now superceded by the fact that linux has a full fledge GUI and system tray app that is very easy to use, but I will keep the command line options for those that want to know what they are.

Status
```
sudo systemctl status xkeysnail
```

Stop (your keymap will return to normal)
```
sudo systemctl stop xkeysnail
```

Start
```
sudo systemctl start xkeysnail
```

Restart
```
sudo systemctl restart xkeysnail
```

## Troubleshooting

### Installed successfully, but modifier keys are not properly remapped?

Are you using a VM on macOS? If so you may need to disable automatic remapping of the Cmd key when using Vmware Fusion of Parallels.

Disable Parallels Re-mapping:
1) Open Parallels and go to Preferences.
2) Click Keyboard and disable the Virtual machine shortcuts.
3) Close Preferences.

To disable keyboard mapping:
1) From Fusion's menu bar, click VMware Fusion > Preferences...
2) Click Keyboard & Mouse.
3) Click the Key Mappings tab.
4) Deselect Enable Key Mapping.

### Does not start when you log in or after you reboot?

You may need to manually set your DISPLAY in the systemd service file. Normally it pulls in the proper DISPLAY value but if it doesn't you can try this.

Another possibility is the SELinux could be enabled and needs to be set to permissive. (aka /etc/selinux/config)

To reset the display variable

```
echo $DISPLAY

# :0.0
```

You can use the Kinto.sh app or system tray to edit your service file.

kinto.sh gui
1. Edit -> Edit Service
kinto tray
1. Customize -> Edit Service

or you can use your terminal.

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

## Language Support
I'd appreciate any help from people with non-US based keyboards, to help ensure that these keymaps and keyswap methods work in all or most languages.

## Related or Useful Resources

[Xkeysnail](https://github.com/mooz/xkeysnail) by mooz

Yet another keyboard remapping tool for X environment

[libinput-gestures](https://github.com/bulletmark/libinput-gestures)
Three finger gesture or other type of gestures for desktop switching or other features within a Linux distro. More info here for quickly setting it up. Make sure you logoff after setting your user to access input. https://www.reddit.com/r/GalliumOS/comments/5lgrxe/psa_multitouch_gestures_on_galliumos/

[Interception](https://gitlab.com/interception/linux/tools)

Another low level key remapper, not as easily configurable as Xkeysnail, but does not rely on X11.

[Wincent](https://github.com/wincent/wincent) by Greg Hurrell

Dot files and configurations that may help those that want mac-style shortcut keys that work under Wayland, or w/o x11.
[Vim #102: macOS keyboard bindings on Linux](https://www.youtube.com/watch?v=TBqTHesnzkI)

[mac-precision-touchpad](https://github.com/imbushuo/mac-precision-touchpad) by imbushuo

Windows 10 touchpad to precision touchpad driver

[macOS-cursors-for-Windows](https://github.com/antiden/macOS-cursors-for-Windows) by antiden

macOS cursors for Windows

[QuickLook](https://github.com/QL-Win/QuickLook) for Windows by QL-Win

It allows users to peek into a file content in lightning speed by just pressing the Space key

[fusuma](https://github.com/iberianpig/fusuma) by iberianpig

Multitouch gestures with libinput driver on Linux

[Facetime HD Camera for Linux](https://github.com/patjak/bcwc_pcie) by patjak

Linux driver for Facetime HD on macbooks

[Windows Terminal Preview](https://aka.ms/terminal-preview) by Microsoft

The best Terminal app built for Windows hands down. I have tried countless, but this one actually seems to get everything right, despite the lack of a GUI to configure all aspects of the program. Custom configurations have to be done via a json file - but given the performance and feature set I feel like it is the a decent trade off.

I will update Kinto to have custom configurations for this specific Terminal in the future. Will make seamless copy & paste, which already works, work even better (Cmd-C can still trigger sigint - but there is a fix for that that involves updating the json config).

[PowerToys - Windows only](https://github.com/microsoft/PowerToys) by microsoft

Windows system utilities to maximize productivity

[AutoHotKey - Windows only](https://github.com/AutoHotkey/AutoHotkey) by AutoHotkey

AutoHotkey is a powerful and easy to use scripting language for desktop automation on Windows.

[pykeymacs](https://github.com/zhanghai/pykeymacs) by zhanghai

Emacs style keyboard macros implemented in Python

[Dynamic Wallpapers](https://github.com/adi1090x/dynamic-wallpaper) by adi1090x

Simple bash script to set a Dynamic Wallpaper according to certain conditions.

[macify-linux](https://github.com/Jonchun/macify-linux) by JonChun

Automated setup scripts to transform Linux into macOS. (Uses Kinto for key remaps)

[ibus-typing-booster](https://github.com/mike-fabian/ibus-typing-booster) by mike-fabian

ibus-typing-booster is a completion input method for faster typing

[twemoji color font](https://github.com/eosrei/twemoji-color-font) by eosrei

Twitter Unicode 12 emoji color SVGinOT font for Linux/MacOS/Windows

[iTerm2 Color Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes) by mbadolato

Over 225 terminal color schemes/themes for iTerm/iTerm2. Includes ports to Terminal, Konsole, PuTTY, Xresources, XRDB, Remmina, Termite, XFCE, Tilda, FreeBSD VT, Terminator, Kitty...

[espanso](https://github.com/federico-terzi/espanso) by federico-terzi

Cross-platform Text Expander written in Rust

[GalliumOS](https://github.com/GalliumOS/galliumos-distro) by GalliumOS

Docs, issues, and artwork sources for GalliumOS

[eOS-X](https://github.com/ipproductions/eOS-X) by ipproductions

Dark & Light Theme w/ OSX controls for Elementary OS

[Autorandr](https://github.com/phillipberndt/autorandr) by phillipberndt

Auto-detect the connected display hardware and load the appropriate X11 setup using xrandr

[Barrier](https://github.com/debauchee/barrier) by debauchee (Note: Does not appear to work with Kinto v1.2+, may work w/ Kinto v1.1?)

Open-source KVM software

[Synergy Free Binaries](https://github.com/amankhoza/synergy-binaries) by amankhoza

The latest freely available Synergy binaries

[Synergy Official](https://symless.com/) by Symless

Latest Official Synergy

[Karabiner-Elements](https://github.com/pqrs-org/Karabiner-Elements) by pqrs-org

Karabiner-Elements is a powerful utility for keyboard customization on macOS Sierra (10.12) or later. 

[mbpfan](https://github.com/linux-on-mac/mbpfan) by linux-on-mac

A simple daemon to control fan speed on all MacBook/MacBook Pros (probably all Apple computers) for Linux Kernel 3 and newer

[vala-panel](https://github.com/rilian-la-te/vala-panel) by rilian-la-te

Vala rewrite of SimplePanel - GitHub mirror (Global Menu for XFCE)

## Contributing

I welcome any and all contributors who want to add something to this project.

You can read the configuration files and the open issue tickets such as [#44 Shortcut Translation Tables](https://github.com/rbreaves/kinto/issues/44), [#115 Shortcut Creation (xkeysnail)](https://github.com/rbreaves/kinto/issues/115), and [#348 Missing Shortcuts: Post them here](https://github.com/rbreaves/kinto/issues/348) to best understand what's currently happening and how best to contribute.

## More information about Kinto

https://medium.com/@benreaves/kinto-v1-0-released-2018e6401d2e
https://medium.com/@benreaves/kinto-a-mac-inspired-keyboard-mapping-for-linux-58f731817c0

## License

GPL v2

## Credits and Contributions

I would just like to thank a few people here directly that have helped me tremendously with completing this project and without their support, direct, indirect or otherwise I would have had difficulty completing this undertaking. I will list these things off in chronological order mostly.

First off I'd like to thank the Stackoverflow and Stackexchange community. I have probably rubbed some mods the wrong way over there, but the people from the community in general are extremely helpful and gracious and without their contributions would have made this much more difficult. The person I'd like to thank most though from over there is Glen Whitney. Without his detailed explaining of how to rebind keys in xkb this would not have come together at all, as every other remapping solution were non-starters as complexity increases. *Kinto today no longer uses xkb, but Glen Whitney did provide the basis of a workable method that helped me pursue this method and think it was a worthwhile project to pursue, so for that I thank him.*

Secondarily I'd like to thank Christian Eriksson*, as he provided information that kept me up at night.. literally. Even after I implemented a similar bash script to one he had suggested I knew that fully implementing a c/c++ solution was where Kinto needed to head to and his explaination was better than I remember it being now that I have gone back to read it again. He also never provided a full implementation of a c/c++ solution - he did hit on the pain points pretty well of what one would need to do and watch out for. I am not sure where I got the first example code of implementing a c based solution, but he definitely went over it well.


Kui and his gist file** was really the c based solution that I found had the fewest issues to resolve to making it a reliable solution. It didn't account for all failures very well, aka BadWindow issues, but it made for a great foundation on which Kintox11 is built. I cannot thank him enough for putting it out there for others to work with.

Lastly these four people were also very helpful to me as well. @probonopd for being one of the first people to install and use Kinto and gave me the initial feedback to include wordwise support! He also has really great articles*** posted on HackerNews & Medium about UI/UX design. Another person I'd like to thank is @owzim, his feedback allowed me to rapidly iterate and fix several bugs to support additional platforms better. The last two are members of the #ubuntu channel in IRC on freenode, tarzeau ( @alexmyczko ) and sarnold. Alex contributing a proper Makefile, so the project can be packaged properly, and sarnold help me find that IBus could resolve an issue I was having with needing to detect the caret status.

**Updated 6/13/2020**

I would also like to thank Jonathan Chun for his patience in helping me work through a very difficult problem related to Alt-Tab switching, which led to the current xkeysnail iteration of Kinto for Linux that far exceeds the original xkb implementation. There are also several others that have created issue tickets that have contributed greatly.

If I left anyone out then I apologize, that was not intentional. I am happy to say that this project is at a state of completion. Bug fixes will primarily be the only activity happening going forward and possibly a rewrite for Wayland at some point. Contributions as mentioned above are welcomed, and will be merged into master if they help with the goal of making typing on linux more like a mac.

*https://askubuntu.com/questions/1010276/can-i-act-on-the-event-that-a-window-opens-without-polling

**https://gist.github.com/kui/2622504

***https://medium.com/@probonopd/make-it-simple-linux-desktop-usability-part-1-5fa0fb369b42
