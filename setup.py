#!/usr/bin/env python3
import json, time, os, sys
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

dename = cmdline("./system-config/dename.sh").replace('"','').strip().split(" ")[0].lower()

def requirements(pkgm):
	print(bcolors.CYELLOW + "You need to install some packages, " +run_pkg+ ", for Kinto to fully remap browsers during input focus.\n" + bcolors.ENDC)
	print("sudo " + pkgm + " " + run_pkg + "\n")
	run_install = yn_choice(bcolors.CYELLOW + "Would you like to run it now? (Will require sudo privileges.)\n" + bcolors.ENDC)
	if(run_install):
		os.system("sudo " + pkgm  + run_pkg)
		print("\n")

def install_ibus():
	print(bcolors.CYELLOW + "You need to set IBus as the default Input Method for full word-wise support and re-run this installer.\n" + bcolors.ENDC)
	print(bcolors.CYELLOW + "Confirm the IBus Setup by saying Yes and then closing the window.\n" + bcolors.ENDC)
	print("ibus-setup\n")
	print("im-config -n ibus\n")
	run_install = yn_choice(bcolors.CYELLOW + "Would you like to run it now? (Will require logoff and logon.)\n" + bcolors.ENDC)
	if(run_install):
		os.system("ibus-setup")
		os.system("im-config -n ibus")
		print("\n")
		input("IBus has been set as the default Input Method.\nPress any key to exit and re-run after logoff & logon...")
		sys.exit()

def setShortcuts():
	distro = cmdline("awk -F= '$1==\"NAME\" { print $2 ;}' /etc/os-release").replace('"','').strip().split(" ")[0]
	distroVersion = cmdline("awk -F= '$1==\"VERSION_ID\" { print $2 ;}' /etc/os-release").replace('"','').strip()
	
	print("\nIf Kinto is already running it will be stopped...")
	print("If you cancel the installer you can re-run Kinto via\n systemctl --user start keyswap")

	cmdline("systemctl --user stop keyswap")
	print("\nDetected " + distro + " " + distroVersion.strip() + " DE: " + dename + "\n")
	addhotkeys = yn_choice("\nDo you want to apply system level shortcuts?")
	if(addhotkeys):
		distro = distro.lower()
		if dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>F13','<Primary><Shift>F13','<Alt>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary>F14','<Primary><Shift>F14','<Alt><Shift>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
		if distro == "ubuntu" and dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up \"['<Super>Up','<Super>Left']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down \"['<Super>Down','<Super>Right']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
		elif distro == "pop!_os" and dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings close \"['<Alt>F4','<Super>w']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings toggle-maximized \"['<Alt>F10','<Primary><Super>Up']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up \"['<Super>Up','<Super>Left']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down \"['<Super>Down','<Super>Right']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ['']")
		elif distro == "elementary" and dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>F13','<Primary><Shift>F13','<Alt>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary>F14','<Primary><Shift>F14','<Alt><Shift>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings show-desktop \"['<Super>d','<Super>Down']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings toggle-maximized \"['<Alt>F10','<Super>Up']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Control><Shift>Space','<Super>Space']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Super>Space','<Primary>Space']\"")
			cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Elementary cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_term')
			cmdline('perl -pi -e "s/(\w.*)(\/\/ Default cmdtab)/\/\/ \$1\$2/g" ~/.xkb/symbols/mac_term')
			cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Elementary cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_gui')
			cmdline('perl -pi -e "s/(\w.*)(\/\/ Default cmdtab)/\/\/ \$1\$2/g" ~/.xkb/symbols/mac_gui')
		elif distro == "galliumos" and dename == "xfce":
			print("Applying GalliumOS (xfce) shortcuts...")
			# Reset Show desktop
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>d" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Super>d" --create --type string --set "show_desktop_key"')
			# Reset App Cycle
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Alt>Tab" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Alt><Shift>Tab" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary>backslash" --create --type string --set "cycle_windows_key"')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Shift>backslash" --create --type string --set "cycle_reverse_windows_key"')
			# cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Super>h" --create --type string --set "hide_window_key"')
			# Don't need to undo other maps for menu
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary>space" --create --type string --set "xfce4-popup-whiskermenu"')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary><Shift>space" --create --type string --set "xfce4-popup-whiskermenu"')
			# Reset move to desktop shortcuts
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Home" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>End" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Left" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Right" --reset')
			os.system('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Left" --create --type string --set "move_window_prev_workspace_key"')
			os.system('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Right" --create --type string --set "move_window_next_workspace_key"')
			# Reset Change Workspace
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Left" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Right" --reset')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Super>Left" --create --type string --set "left_workspace_key"')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Super>Right" --create --type string --set "right_workspace_key"')
			print("\nYou may need to run these commands manually to make sure they are set, if you want to move windows between desktops.\n")
			print('     xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Left" --create --type string --set "move_window_prev_workspace_key"')
			print('     xfconf-query --channel xfce4-keyboard-shortcuts --property "/xfwm4/custom/<Primary><Alt>Right" --create --type string --set "move_window_next_workspace_key"\n')
		elif distro == "fedora" and dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings show-desktop \"['<Super>d']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up \"['<Super>Up','<Super>Left']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down \"['<Super>Down','<Super>Right']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
			cmdline("gsettings set org.gnome.mutter.keybindings toggle-tiled-right \"['<Super><Alt>Right']\"")
			cmdline("gsettings set org.gnome.mutter.keybindings toggle-tiled-left \"['<Super><Alt>Left']\"")
			# org.gnome.mutter.keybindings toggle-tiled-right ['<Super>Right']
			# org.gnome.mutter.keybindings toggle-tiled-left ['<Super>Left']
		elif dename == "kde":
			# cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "krunner.desktop" --key "_launch","Alt+Space\tAlt+F2\tSearch,Alt+Space\tAlt+F2\tSearch,KRunner"')
			# Remove Alt+F3 Operations Menu - Sublimetext Select-All
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Switch to Previous Desktop" "Meta+Left,Meta+Left,Switch to Previous Desktop"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Operations Menu" "none,Alt+F3,Window Operations Menu"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows" "Ctrl+F13,Alt+Tab,Walk Through Windows"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows (Reverse)" "Ctrl+Shift+F14,Alt+Shift+Backtab,Walk Through Windows (Reverse)"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Maximize Window" "none,Meta+PgUp,Maximize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Maximize" "Meta+Ctrl+F,Alt+F10,Maximize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Minimize Window" "Meta+h,Meta+PgDown,Minimize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Switch to Next Desktop" "Meta+Right,Meta+Right,Switch to Next Desktop"')
			os.system('kquitapp5 kglobalaccel && sleep 2s && kglobalaccel5 &')
		else:
			print('distro: ' + distro + ' de: ' + dename)
			print("A supported OS and DE was not found, you may not have full system level shortcuts installed.")

def windows_setup():
	keymaps = ["Apple keyboard standard", "Apple keyboard w/ Caps lock as Esc", "Windows keyboard standard", "Windows keyboard w/ Caps lock as Esc","Uninstall"]
	for index, item in enumerate(keymaps):
		print("    %i. %s" % (index+1, item.capitalize()))
	default = 0
	while not int(default) in range(1,len(keymaps)+1):
		default = int(input("\nPlease enter your desired keymap (1 - " + str(len(keymaps)) + ") : "))
	print("")
	path= cmdline('echo %cd%')[:-1]
	if default == 1:
		os.system("regedit " + path + "\\windows\\macbook_winctrl_swap.reg")
	elif default == 2:
		os.system("regedit " + path + "\\windows\\macbook_winctrl_capsesc_swap.reg")
	elif default == 3:
		os.system("regedit " + path + "\\windows\\standard_ctrlalt_swap.reg")
	elif default == 4:
		os.system("regedit " + path + "\\windows\\standard_ctrlalt_capsesc_swap.reg")
	elif default == 5:
		os.system("regedit " + path + "\\windows\\remove_keyswap.reg")
	if default > 0 and default < 5:
		print("Will now install chocolatey and autohotkey with elevated privileges...")
		print("This install will fail if you are not running with elevated privileges")
		os.system('powershell -executionpolicy bypass ".\\windows\\autohotkey.ps1"')
		print("\nWill now install Ubuntu Terminal Theme as default...")
		os.system("regedit " + path + "\\windows\\theme_ubuntu.reg")
		print("Copying autohotkey combinations for Terminals & Editors...")
		os.system("copy /Y " + path + "\\windows\\kinto.ahk \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kinto.ahk\"")
		print("\nPlease log off and back on for changes to take full effect.")
		print("If using WSL then please remember to right click on title bar -> Properties -> Edit Options -> Use Ctrl+Shift+C/V as Copy/Paste and enable it.")
	else:
		os.system("del \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kinto.ahk\"")

# check_x11 = cmdline("env | grep -i x11").strip()
check_x11 = cmdline("(env | grep -i x11 || loginctl show-session \"$XDG_SESSION_ID\" -p Type) | awk -F= '{print $2}'").strip()

if len(check_x11) == 0:
	if os.name != 'nt':
		print("You are not using x11, please logout and back in using x11/Xorg")
		sys.exit()
	else:
		print("You are detected as running Windows.")
		windows_setup()
		sys.exit()

check_xbind = cmdline("which xbindkeys 2>/dev/null").strip()
check_xdotool = cmdline("which xdotool 2>/dev/null").strip()
check_ibus = cmdline("which ibus-setup 2>/dev/null").strip()

pkgm = cmdline("which apt-get 2>/dev/null").strip()

if len(pkgm) == 0:
	pkgm = cmdline("which dnf 2>/dev/null").strip()
	if len(pkgm) > 0:
		pkgm += " check-update;sudo dnf install -y "
else:
	pkgm += " install -y "
	pkgm += " update; sudo apt-get install -y "

if len(pkgm) == 0:
	pkgm = cmdline("which pacman 2>/dev/null").strip()
	if len(pkgm) > 0:
		pkgm += " -Syy; sudo pacman -S "


if len(pkgm) == 0:
	print("No supported package manager found. Exiting...")
	sys.exit()


runpkg = 0
run_pkg = ""

if len(check_xbind) > 0 and len(check_xdotool) > 0 and len(check_ibus) > 0:
	print("Xbindkeys, xdotool and IBus requirement is installed.")
if len(check_xbind) == 0:
	run_pkg = "xbindkeys"
	runpkg = 1
if len(check_xdotool) == 0:
	run_pkg += " xdotool"
	runpkg = 1
if len(check_ibus) == 0:
	# may differ with distro, but for now
	run_pkg += " ibus"
	runpkg = 1

if runpkg != 0:
	requirements(pkgm)

if not os.path.exists(homedir + '/.config/ibus/bus') and cmdline("ls ~/.config/ibus/bus -1rt") == "":
	install_ibus()

try:
	f = open("defaults.json")
except IOError:
	print("defaults.json file is missing. Will exit.\n")
	exit()
f.close()

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
os.system("cp -TRv ./.xkb ~/.xkb/")
if os.path.isdir(homedir + "/.xkb/keymap") == False:
	os.mkdir(homedir + "/.xkb/keymap")
	time.sleep(0.5)
os.system('setxkbmap -option')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui.chrome')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.gui.browsers')
os.system('setxkbmap -print > ~/.xkb/keymap/kbd.mac.term')
time.sleep(0.5)

symbols_line = cmdline("cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_symbols' | cut -f1 -d:").strip()
types_line = cmdline("cat ~/.xkb/keymap/kbd.mac.gui | grep -n 'xkb_types' | cut -f1 -d:").strip()

cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui')
cmdline('sed -i '' -e "' + types_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_types_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui')
cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_term'] + '\\"/2" ~/.xkb/keymap/kbd.mac.term')
cmdline('sed -i '' -e "' + types_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_types_term'] + '\\"/2" ~/.xkb/keymap/kbd.mac.term')

# Set chrome file accordingly for chromebooks or normal
if default != 3:
	cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'].replace("+mac_gui(mac_levelssym)+mac_gui(mac_appcycle)","+mac_gui(mac_levelssym)+mac_gui(mac_browsers)") + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.browsers')
	cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'].replace("+mac_gui(mac_levelssym)+mac_gui(mac_appcycle)","+mac_gui(mac_browsers)+mac_gui(mac_chrome)") + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.chrome')
else:
	# Fix multicursor in mac_gui
	cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Chromebook multicursor)/\$2\$3/g" ~/.xkb/symbols/mac_gui')
	cmdline('perl -pi -e "s/(\w.*)(\/\/ Default multicursor)/\/\/ \$1\$2/g" ~/.xkb/symbols/mac_gui')
	# Fix browsers
	cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'].replace("+mac_gui(mac_levelssym)+mac_gui(mac_appcycle_chromebook)","+mac_gui(mac_levelssym)+mac_gui(mac_browsers_chromebook)") + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.browsers')
	cmdline('sed -i '' -e "' + symbols_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_symbols_gui'].replace("+mac_gui(mac_levelssym)+mac_gui(mac_appcycle_chromebook)","+mac_gui(mac_browsers_chromebook)+mac_gui(mac_chrome)") + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.chrome')
if dename == "kde":
	# Fix maximize shortcut
	cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ KDE maximize)/\$2\$3/g" ~/.xkb/symbols/mac_gui')
	# term app switching
	cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ KDE cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_term')
else:
	# Fix maximize shortcut
	cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Default maximize)/\$2\$3/g" ~/.xkb/symbols/mac_gui')
	# term app switching
	cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Default cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_term')
cmdline('sed -i '' -e "' + types_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_types_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.browsers')
cmdline('sed -i '' -e "' + types_line + 's/\\"/' + keyboardconfigs[defaultkb-1]['xkb_types_gui'] + '\\"/2" ~/.xkb/keymap/kbd.mac.gui.chrome')

setShortcuts()

user_file = homedir + '/.config/kinto/user_config.json'
with open(user_file, 'r') as f:
    user_config = json.load(f)

onetime = yn_choice("\nOne time initialization tweaks are available. Would you like to view them?")
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
		user_config['init'] = [intents[defaultinit[0]-1]['id']]

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
	# firefox
	user_config['config'][2]['de'] = tweaks_selected
	# chrome
	user_config['config'][3]['de'] = tweaks_selected

user_config['config'][0]['run'] = keyboardconfigs[defaultkb-1]['gui']
user_config['config'][1]['run'] = keyboardconfigs[defaultkb-1]['term']
user_config['config'][2]['run'] = keyboardconfigs[defaultkb-1]['gui'].replace("kbd.mac.gui","kbd.mac.gui.browsers")
user_config['config'][3]['run'] = keyboardconfigs[defaultkb-1]['gui'].replace("kbd.mac.gui","kbd.mac.gui.chrome")

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