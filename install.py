#!/usr/bin/env python3
import os, platform, sysconfig, sys, subprocess

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
print()
print("Checking for OS and system information...")
print()
print("OS Type")
# print(" Platform: " + platform_name)
if platform_name == 'Linux':
    result = subprocess.check_output("lsb_release -a | grep -v LSB ", shell=True).decode('ascii')
    print(result)
print()
print("Looking for keyboards...")
print()
result = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard";exit 0', shell=True).decode('utf-8')
if result != "":
    print("Built in keyboard")
    print(result)

result = subprocess.check_output('udevadm info -e | grep -o -P "(?<=by-id/usb-).*(?=-event-kbd)" | head -1;exit 0', shell=True).decode('utf-8')
if result != "":
    print("USB keyboard")
    print(result)

internalid = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard" | cut -d "=" -f 2- | awk \'{print $1}\';exit 0', shell=True).decode('utf-8')

# Loop the following to ensure the id is picked up after 5-10 tries
usbid = subprocess.check_output('udevadm info -e | stdbuf -oL grep -o -P "(?<=event-kbd /dev/input/by-path/pci-0000:00:).*(?=.0-usb)";exit 0', shell=True).decode('utf-8')
if usbid == "":
    usbid = "none found"


print("Internal Keyboard ID: " + internalid + "USB Keyboard ID: " + usbid)

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

