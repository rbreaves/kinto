#!/usr/bin/env python3
import os, platform, sysconfig, sys, subprocess, time

yellow = "\033[1;33m"
green = "\033[0;32m"
red = "\033[1;31m"
italic = "\033[3m"
reset = "\033[0;0m"

platform_name = platform.system()
# print sysconfig.get_platform()

sys.stdout.write(yellow)
cloud = '\u2601'
circleo = '\u25CE'
clocko = '\u2B6E'
syme = '\u0250'
syma = '\u0251'
# bang = '\u1F589'.decode('unicode-escape')

internalid = 0
usbid = 0

def keyboard_detect():
    global internalid, usbid, chromeswap
    internal_kbname = ""
    usb_kbname = ""
    print()
    print("Looking for keyboards...")
    print()
    result = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard" | grep -o -P "(?<=↳).*(?=id\=)";exit 0', shell=True).decode('utf-8')
    if result != "":
        internal_kbname = result.strip()
    internalid = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard" | cut -d "=" -f 2- | awk \'{print $1}\';exit 0', shell=True).decode('utf-8')
    print("Internal Keyboard\nName: " + internal_kbname + "\nID: " + internalid)

    result = subprocess.check_output('udevadm info -e | grep -o -P "(?<=by-id/usb-).*(?=-event-kbd)" | head -1;exit 0', shell=True).decode('utf-8')
    if result != "":
        usb_kbname = result.strip()

    # Loop the following to ensure the id is picked up after 5-10 tries
    usbid = ""
    usbcount=0
    while usbid == "":
        usbid = subprocess.check_output('udevadm info -e | stdbuf -oL grep -o -P "(?<=event-kbd /dev/input/by-path/pci-0000:00:).*(?=.0-usb)";exit 0', shell=True).decode('utf-8')
        if usbid == "":
            usbcount += 1
            # print('usbid not found '+ str(usbcount))
            if usbcount == 5:
                usbid = "none found"
        time.sleep(1)
    print("\nUSB Keyboard\n" + "Name: " + usb_kbname + "\nID: " + usbid)
        


def os_detect():
    print()
    print("Checking for OS and system information...")
    print()
    print("OS Type")
    # print(" Platform: " + platform_name)
    if platform_name == 'Linux':
        result = subprocess.check_output("lsb_release -a | grep -v LSB ", shell=True).decode('ascii')
        print(result)

def hwinfo():
    print("Requires user password to display hardware information...")
    result = subprocess.check_output('sudo dmidecode | grep -A 9 "System Information" | grep -v "UUID\|Serial\|SKU\|Wake"', shell=True).decode('ascii')
    print(result)

def kblist():
    result = subprocess.check_output('xinput list', shell=True).decode('ascii')
    print(result)

print()
print()
print("                      K!nt" +  circleo)
sys.stdout.write(reset)
print(italic + "            - F!x the d" + syma + "mn k" + syme + "yb" + circleo + syma + "rd. - ")
sys.stdout.write(reset)
print()
input("Press Enter to begin...")

system_type = input("\nWhat type of system are you using?\n\
    1) Windows\n\
    2) Chromebook\n\
    3) Mac\n")

swap_behavior = 1
# Chromebook
if system_type == "2":
    if input("\nWould you like to swap Alt to Super/Win and Search key to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0
# Windows
if system_type == "1":
    if input("\nWould you like to swap Alt to Super/Win and Ctrl key back to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0
# Mac
if system_type == "3":
    if input("\nWould you like to swap Command back to Super/Win and Ctrl key back to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0

print(system_type + " " + str(swap_behavior))
if int(system_type) == 2 and swap_behavior == 0:
    chromeswap = input("\nIf the keyswap is applied on a chromebook with both an internal and external Apple keyboard\n\
you may need to press a key on the external Apple keyboard any time you switch between the terminal and gui based apps.\n\
Are you ok with that, or would you like to only apply the keyswap on one keyboard type?\n\
    1) Built-in\n\
    2) Both - (Chromebook & Windows)\n\
    3) Both - (Chromebook & Mac)\n\
    4) USB External - (Mac)\n")

keyboard_detect()

# terminal_kb 

# os_detect()


# Print out/confirm the keyboard type or types detected, Windows, Mac, or Chromebook.
# Print out the keymap method/arrangement that will be used for the keyboard(s)
# - Normal apps - Alt will be Ctrl, Win/Super will be Alt, Ctrl will be Win/Super
# - Terminal apps (optional) - Alt will be Win/Super, Win/Super will be Alt, Ctrl will be Ctrl
#
# If Chromebook then create a local symbols file for swapping ctrl and alt.
# - setxkbmap -print > ~/.xkb/keymap/kbd.gui
# - modify ~/.xkb/keymap/kbd.gui xkb_symbols line with +myswap(swap_lalt_lctrl) inside the quotes at the end
# - create/copy lalt_lctrl to ~/.xkb/symbols/myswap
#
# Ask user how they would like their keymap to work
# 2 options will be given 
# 1) Mac like option - Normal swap, but swap alt with super when the terminal is in use, so ctrl key behaves normally.
# 2) Always swapped - Always keep alt as ctrl.
#
# Begin test run on Internal Keyboard, have user confirm that it is correct
# Begin test run on External Keyboard, if one was attached, again ask user for confirmation
# Note: The test may use xev to confirm the key input.
# Ask user if they would like to apply Kinto persistently, run as a service
#
# - Windows keyboards
#   - gui - setxkbmap -option altwin:ctrl_alt_win
#   - terminal -  setxkbmap -option altwin:swap_alt_win
# - Mac keyboards
#  - gui - setxkbmap -option ctrl:swap_lwin_lctl
#  - terminal - setxkbmap -option
# - Chromebook keyboard
#  - gui - xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.gui $DISPLAY
#  - terminal - setxkbmap -option altwin:swap_lalt_lwin
#
# Ask User if they would like Kinto to hook into udev/usb/hid to create persistent remaps for any keyboard
# If yes then create a file to hook into any udev/usb/hid keyboard devices when plugged in.

# Add autohotkey scripts to handle keymapping for Windows

