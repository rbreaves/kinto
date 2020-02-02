#!/usr/bin/env python3

import json
import os
from subprocess import PIPE, Popen
from shutil import copyfile
from prekinto import *

print("\nKinto - Type in Linux like it's a Mac.\n")

try:
	f = open("default.json")
except IOError:
	print("default.json file is missing. Will exit.\n")
	exit()
f.close()

try:
	f = open("kinto.json")
	rewrite = yn_choice("kinto.json already exists. Do you want to overwrite it with a new config?")
	print("")
	if(rewrite):
		copyfile("default.json", "kinto.json")
	else:
		exit()
except IOError:
	pass
	copyfile("default.json", "kinto.json")
finally:
    f.close()

with open('kinto.json') as json_file:
	data = json.load(json_file)

	for index, item in enumerate(data['defaulttypes']):
		ossym = ""
		color_arr = [bcolors.CBLUE,bcolors.CRED,bcolors.CGREEN]
		if item == "windows":
			ossym = u'\u2756'
		elif item == "mac":
			ossym = u'\u2318'
		elif item == "chromebook":
			ossym = u'\u2707'
		print("%s    %i. %s  %s %s" % (color_arr[index], index+1, ossym, item.capitalize(), bcolors.ENDC))

	default = 0
	while not int(default) in range(1,len(data['defaulttypes'])+1):
		default = int(input(bcolors.CYELLOW + "Please enter your keyboard type (1 - " + str(len(data['defaulttypes'])) + ") : " + bcolors.ENDC))
	print("")
	# print(data['defaulttypes'][default-1])

	keyboardconfigs = [obj for obj in data['defaults'] if(obj['type'] == data['defaulttypes'][default-1])]
	# print(len(keyboardconfigs))

	# for k in keyboardconfigs:
	for index, k in enumerate(keyboardconfigs):
		print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
		print(bcolors.CYELLOW + 'Description: ' + k['description'] + bcolors.ENDC)

	# print(keyboardconfigs[0]['id'])
	# print(keyboardconfigs[len(keyboardconfigs)-1]['id'])
	print("")
	defaultkb = 0
	while not int(defaultkb) in range(1,len(keyboardconfigs)+1):
		defaultkb = int(input(bcolors.CYELLOW + "Please enter your keyboard config (1 - " + str(len(keyboardconfigs)) + ") : " + bcolors.ENDC))
	print("")

	if 'hack' in keyboardconfigs[defaultkb-1]:
		print(bcolors.CYELLOW + "You have selected a keyboard config that needs the following command to be ran.\n" + bcolors.ENDC)
		print(keyboardconfigs[defaultkb-1]['hack'].replace(";", "\n") + "\n")
		runhack = yn_choice(bcolors.CYELLOW + "Would you like to run it now? (Will require sudo privileges. Will exit on No.)" + bcolors.ENDC)
		if(runhack):
			# keyboardconfigs[defaultkb-1]['hack']
			os.system('sudo hostname')
		# else:
		# 	exit()

	# Setup the selected keyboards config
	copytree("./.xkb/","~/.xkb/")
	os.system('setxkbmap -option')
	os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui')
	os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.term')
	winmac = ["Windows","Mac - hid driver"]
	if keyboardconfigs[defaultkb-1]['name'] in winmac:


# line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_symbols' | cut -f1 -d:)
# sed -ie "${line}s/\"/+altwin(ctrl_alt_win)+mac_gui(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.mac.gui
# sleep 1
# line=$(cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:)
# sed -ie "${line}s/\"/+mac_gui(addmac_levels)\"/2" ~/.xkb/keymap/kbd.mac.gui
# sleep 1
# line=$(cat ~/.xkb/keymap/kbd.mac.term | grep -n 'xkb_symbols' | cut -f1 -d:)
# sed -ie "${line}s/\"/+altwin(swap_alt_win)+mac_term(mac_levelssym)\"/2" ~/.xkb/keymap/kbd.mac.term
		

# Tweaks available for initialization (on boot)

# Tweaks available while in gui keymap mode

# Tweaks available while in terminal keymap mode


# "id": 2,
# "name":"Mac - hid driver",
# "active": false,
# "description":"Standard Mac Keyboards with Apple driver",
# "gui":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY",
# "term":"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.term $DISPLAY",
# "xkb_symbols_gui":"+altwin(ctrl_alt_win)+mac_gui(mac_levelssym)",
# "xkb_symbols_term":"+altwin(swap_alt_win)+mac_term(mac_levelssym)",
# "xkb_types_gui":"+mac_gui(addmac_levels)",
# "xkb_types_term":"",
# "hack": "echo '1' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd;echo 'options hid_apple swap_opt_cmd=1' | sudo tee -a /etc/modprobe.d/hid_apple.conf;sudo update-initramfs -u -k all"

