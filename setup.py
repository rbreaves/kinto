#!/usr/bin/env python3
import json, time, os
from shutil import copyfile
from subprocess import PIPE, Popen
from prekinto import *

homedir = os.path.expanduser("~")

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        universal_newlines=True,
        shell=True
    )
    return process.communicate()[0]

try:
	f = open("defaults.json")
except IOError:
	print("defaults.json file is missing. Will exit.\n")
	exit()
f.close()

try:
	f = open("user_config.json")
except IOError:
	print("user_config.json file is missing. Will exit.\n")
	exit()
f.close()

if os.path.isdir(homedir + "/.config/kinto") == False:
	os.mkdir(homedir + "/.config/kinto")
	time.sleep(0.5)

try:
	f = open(homedir + "/.config/kinto/user_config.json")
	rewrite = yn_choice("~/.config/kinto/user_config.json already exists. Do you want to overwrite it with a new config?")
	print("")
	if(rewrite):
		copyfile("user_config.json", homedir + "/.config/kinto/user_config.json")
	else:
		exit()
except IOError:
	pass
	copyfile("user_config.json", homedir + "/.config/kinto/user_config.json")
finally:
    f.close()

with open('defaults.json') as json_file:
	data = json.load(json_file)

color_arr = [bcolors.CBLUE,bcolors.CRED,bcolors.CGREEN]

print("\nKinto - Type in Linux like it's a Mac.\n")

for index, item in enumerate(data['defaulttypes']):
	ossym = ""
	if item == "windows":
		ossym = u'\u2756'
	elif item == "mac":
		ossym = u'\u2318'
	elif item == "chromebook":
		ossym = u'\u2707'
	print("%s    %i. %s  %s %s" % (color_arr[index], index+1, ossym, item.capitalize(), bcolors.ENDC))

default = 0
while not int(default) in range(1,len(data['defaulttypes'])+1):
	default = int(input(bcolors.CYELLOW + "\nPlease enter your keyboard type (1 - " + str(len(data['defaulttypes'])) + ") : " + bcolors.ENDC))
print("")

keyboardconfigs = [obj for obj in data['defaults'] if(obj['type'] == data['defaulttypes'][default-1])]

# for k in keyboardconfigs:
for index, k in enumerate(keyboardconfigs):
	print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
	print(bcolors.CYELLOW + 'Description: ' + k['description'] + bcolors.ENDC)

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
		os.system(keyboardconfigs[defaultkb-1]['hack'])

# Setup the selected keyboards config
os.system("cp -rf ./.xkb ~/.xkb")
if os.path.isdir(homedir + "/.xkb/keymap") == False:
	os.mkdir(homedir + "/.xkb/keymap")
	time.sleep(0.5)
os.system('setxkbmap -option')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.term')
time.sleep(0.5)

symbols_gui_line = cmdline("cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_symbols' | cut -f1 -d:").strip()
types_gui_line = cmdline("cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:").strip()
symbols_term_line = cmdline("cat ~/.xkb/keymap/kbd.mac.term | grep -n 'xkb_symbols' | cut -f1 -d:").strip()

cmdline('sed -i '' -e "' + symbols_gui_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui')
cmdline('sed -i '' -e "' + types_gui_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_types_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui')
cmdline('sed -i '' -e "' + symbols_term_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_term'] + '\\"/2" ~/.xkb/keymap/kbd.mac.term')


user_file = homedir + '/.config/kinto/user_config.json'
with open(user_file, 'r') as f:
    user_config = json.load(f)

onetime = yn_choice("One time initialization tweaks are available. Would you like to view them?")
print("")
if(onetime):
	intents = [obj for obj in user_config['de'] if(obj['intent'] == "init")]

	for index, k in enumerate(intents):
		print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
		print(bcolors.CYELLOW + 'Description: ' + k['description'] + bcolors.ENDC)
		print(bcolors.CYELLOW + 'run: ' + k['run'].replace(";", "\n") + bcolors.ENDC + '\n')

	print(bcolors.CYELLOW + "Please enter your init tweak(s) (eg 1 or 1 2 3 - leave blank to skip): " + bcolors.ENDC)
	defaultinit = [int(i) for i in input().split()]
	if len(defaultinit) != 0:
		user_config['init'] = defaultinit

print("\nDynamic shortcut tweaks\n")

intents = [obj for obj in user_config['de'] if(obj['intent'] == "gui_term")]
tweaks = []
tweaks_selected = []

for index, k in enumerate(intents):
	print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
	print(bcolors.CYELLOW + 'Description: ' + k['description'] + bcolors.ENDC)
	print(bcolors.CYELLOW + 'run in gui mode: ' + k['run_gui'].replace(";", "\n") + bcolors.ENDC)
	print(bcolors.CYELLOW + 'run in terminal mode: ' + k['run_term'].replace(";", "\n") + bcolors.ENDC + '\n')
	tweaks.append(k['id'])

print(bcolors.CYELLOW + "Please enter your dynamic shortcut tweak(s) (eg 1 or 1 2 3 - leave blank to skip): " + bcolors.ENDC)
defaultde = [int(i) for i in input().split()]

for d in defaultde:
    user_config['de'][tweaks[d-1]]['active'] = True
    tweaks_selected.append(tweaks[d-1])

if len(defaultde) != 0:
	# gui
	user_config['config'][0]['de'] = tweaks_selected
	# term
	user_config['config'][1]['de'] = tweaks_selected

user_config['config'][0]['run'] = keyboardconfigs[defaultkb-1]['gui']
user_config['config'][1]['run'] = keyboardconfigs[defaultkb-1]['term']

os.remove(user_file)
with open(user_file, 'w') as f:
    json.dump(user_config, f, indent=4)
print("Saved configuration to ~/.config/kinto/user_config.json\n")
print("Now running keyswap_service.sh to setup the keyswap service...")
print("Keyswap will be configured to run on user login\n")
print("You may start, stop, restart or view the status of the service with following commands\n")
print("systemctl --user start keyswap")
print("systemctl --user stop keyswap")
print("systemctl --user restart keyswap")
print("systemctl --user status keyswap")
os.system("./keyswap_service.sh")