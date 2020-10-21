#!/usr/bin/env python3
import json, time, os, sys, subprocess, shlex, platform
from shutil import copyfile
from subprocess import PIPE, Popen
from prekinto import *

homedir = os.path.expanduser("~")
kintotype = 0

def windows_setup():
	keymaps = ["Apple keyboard standard", "Windows keyboard standard","Chromebook","IBM - No Super/Win","Uninstall"]
	for index, item in enumerate(keymaps):
		print("    %i. %s" % (index+1, item))
	default = 0
	while not int(default) in range(1,len(keymaps)+1):
		default = int(input("\nPlease enter your desired keymap (1 - " + str(len(keymaps)) + ") : "))
	print("")
	# Short DOS path notation
	path= cmdline('echo ''%cd%''')[:-1]
	if default > 0 and default < 5:
		print("Will now install chocolatey and autohotkey with elevated privileges...")
		print("This install will fail if you are not running with elevated privileges")
		os.system('powershell -executionpolicy bypass ".\\windows\\autohotkey.ps1"')
		print("Copying autohotkey combinations for Terminals & Editors...")
		os.system('copy /Y "' + path + '\\windows\\kinto.ahk" "' + path + '\\windows\\kinto-new.ahk"')
	if default < 3:
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Default)(?!( - ST2CODE))(.*)/$2$3$5/g" .\\windows\\kinto-new.ahk')
	if default == 1:
		kbtype = "mac"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; MacModifiers)/$2$3/g" .\\windows\\kinto-new.ahk')
	elif default == 2:
		kbtype = "win"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers)/$2$3/g" .\\windows\\kinto-new.ahk')
	elif default == 5:
		print("Removing any old registry keys from prior versions...")
		p = subprocess.Popen(['powershell.exe', "Remove-ItemProperty -Path HKLM:'SYSTEM\CurrentControlSet\Control\Keyboard Layout' -Name 'Scancode Map' -ErrorAction SilentlyContinue"], stdout=sys.stdout)
		print("Removing Kinto from Startup folder...")
		os.system("(del \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kinto.ahk\") 2> nul")
		os.system('(del "%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\STARTM~1\\Programs\\Startup\\kinto-start.vbs") 2> nul')
		print("Ending any running Kinto tasks...")
		os.system("(taskkill /IM autohotkey.exe) 2> nul")
		print("Removing Kinto from users profile directory...")
		os.system('(rd /s /q "%userprofile%\\.kinto") 2> nul')
		print("")
		print("Uninstall of Kinto is Complete.")
	if default == 3:
		kbtype = "chrome"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Chromebook)/$2$3/g" .\\windows\\kinto-new.ahk')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers/CB)/$2$3/g" .\\windows\\kinto-new.ahk')
	if default == 3 or default == 4:
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; CB/IBM)/$2$3/g" .\\windows\\kinto-new.ahk')
	if default == 4:
		kbtype = "ibm"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; IBM)/$2$3/g" .\\windows\\kinto-new.ahk')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers/CB/IBM)/$2$3/g" .\\windows\\kinto-new.ahk')
	if default > 0 and default < 5:
		stvscode = yn_choice(bcolors.CYELLOW2 + "Would you like to use Sublime Text 3 keymaps in VS Code?\n" + bcolors.ENDC)
		print("\nWill now install Ubuntu Termimnal Theme as default...")
		os.system('regedit "' + path + '\\windows\\theme_ubuntu.reg"')
		os.system('robocopy "'+ path + '\\assets" "%userprofile%\\.kinto\\assets" /E')
		if (stvscode and (default > 0 or default < 3)):
			os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Default - ST2CODE)/$2$3/g" .\\windows\\kinto-new.ahk')
		elif (stvscode and (default == 3 or default == 4 )):
			os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; CB/IBM - ST2CODE)/$2$3/g" .\\windows\\kinto-new.ahk')
		os.system('copy /Y "' + path + '\\windows\\kinto-start.vbs" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/{kbtype}/' + kbtype + '/g" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('copy /Y "' + path + '\\windows\\usb.vbs" "%userprofile%\\.kinto\\usb.vbs"')
		os.system('copy /Y "' + path + '\\windows\\detectUSB.ahk" "%userprofile%\\.kinto\\detectUSB.ahk"')
		os.system('mklink "%userprofile%\\Start Menu\\Programs\\Startup\\kinto-start.vbs" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('copy /Y "'+ path + '\\windows\\NoShell.vbs" "%userprofile%\\.kinto\\NoShell.vbs"')
		os.system('copy /Y "'+ path + '\\windows\\toggle_kb.bat" "%userprofile%\\.kinto\\toggle_kb.bat"')
		os.system('copy /Y "'+ path + '\\windows\\kinto-new.ahk" "%userprofile%\\.kinto\\kinto.ahk"')
		os.system("del /f .\\windows\\kinto-new.ahk")
		os.system("del \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kinto.ahk\" 2> nul")
		userpath = cmdline('cmd /c for %A in ("%userprofile%") do @echo %~sA')[:-1]
		print('Starting... "' + userpath + '\\AppData\\Roaming\\Microsoft\\Windows\\STARTM~1\\Programs\\Startup\\kinto-start.vbs"')
		os.system('"' + userpath + '\\AppData\\Roaming\\Microsoft\\Windows\\STARTM~1\\Programs\\Startup\\kinto-start.vbs"')
	# 	# print("\nPlease log off and back on for changes to take full effect.")
		print("If using WSL then please remember to right click on title bar -> Properties -> Edit Options -> Use Ctrl+Shift+C/V as Copy/Paste and enable it.")
	else:
		os.system("(del \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kinto.ahk\") 2> nul")

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        universal_newlines=True,
        shell=True
    )
    return process.communicate()[0]

if platform.system() == 'Windows':
	print("\nYou are detected as running Windows.")
	windows_setup()
	sys.exit()

check_x11 = cmdline("(env | grep -i x11 || loginctl show-session \"$XDG_SESSION_ID\" -p Type) | awk -F= '{print $2}'").strip()

if len(check_x11) == 0:
	if os.name != 'nt':
		print("You are not using x11, please logout and back in using x11/Xorg")
		sys.exit()
	else:
		print("\nYou are detected as running Windows.")
		windows_setup()
		sys.exit()

distro = cmdline("awk -F= '$1==\"NAME\" { print $2 ;}' /etc/os-release").replace('"','').strip().split(" ")[0]
dename = cmdline("./system-config/dename.sh").replace('"','').strip().split(" ")[0].lower()

run_pkg = ""

def requirements(pkgm):
	print(bcolors.CYELLOW2 + "You need to install some packages, " +run_pkg+ ", for Kinto to fully remap browsers during input focus.\n" + bcolors.ENDC)
	print("sudo " + pkgm + " " + run_pkg + "\n")
	run_install = yn_choice(bcolors.CYELLOW2 + "Would you like to run it now? (Will require sudo privileges.)\n" + bcolors.ENDC)
	if(run_install):
		os.system("sudo " + pkgm  + run_pkg)
		print("\n")

def install_ibus():
	global distro
	print(bcolors.CYELLOW2 + "You need to set IBus as the default Input Method for full word-wise support and re-run this installer.\n" + bcolors.ENDC)
	print(bcolors.CYELLOW2 + "Confirm the IBus Setup by saying Yes and then closing the window.\n" + bcolors.ENDC)
	print("ibus-setup\n")
	print("im-config -n ibus or im-chooser\n")
	run_install = yn_choice(bcolors.CYELLOW2 + "Would you like to run it now? (Will require logoff and logon.)\n" + bcolors.ENDC)
	if(run_install):
		if distro=="fedora":
			os.system("ibus-setup")
			os.system("im-chooser")
			print("\n")
			print("IBus needs to have Input Method set to your language.")
			print("im-chooser needs IBus to be selected & closed.")
			input("Will need to log off and back on for it take effect...")
		else:
			os.system("ibus-setup")
			os.system("im-config -n ibus")
			print("\n")
			input("IBus has been set as the default Input Method.\nPress any key to exit and re-run after logoff & logon...")
		sys.exit()

def setShortcuts():
	global distro
	distroVersion = cmdline("awk -F= '$1==\"VERSION_ID\" { print $2 ;}' /etc/os-release").replace('"','').strip()
	
	print("\nIf Kinto is already running it will be stopped...")
	print("If you cancel the installer you can re-run Kinto via\n systemctl --user start keyswap")

	cmdline("systemctl --user stop keyswap")
	print("\nDetected " + distro + " " + distroVersion.strip() + " DE: " + dename + "\n")
	addhotkeys = yn_choice("\nDo you want to apply system level shortcuts?")
	if(addhotkeys):
		distro = distro.lower()
		if dename == "gnome" or dename == "mate" or dename == "budgie":
			cmdline('dconf dump /org/gnome/desktop/wm/keybindings/ > keybindings_`date +"%Y.%m.%d-%s"`.conf')
			cmdline('dconf dump /org/gnome/mutter/keybindings/ > mutter_`date +"%Y.%m.%d-%s"`.conf')
			if(kintotype == 1):
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>Tools','<Alt>Tab']\"")
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary><Shift>Tools','<Alt><Shift>Tab']\"")
			else:
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>F13','<Primary><Shift>F13','<Alt>Tab']\"")
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary>F14','<Primary><Shift>F14','<Alt><Shift>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			#
			# Leaving run dialog disabled for now
			# Too slow on appearing, compared to the app menu
			#
			# if dename != "budgie":
			cmdline("gsettings reset org.gnome.desktop.wm.keybindings panel-main-menu")
			# cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
			# else:
			# 	cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Alt>F1']\"")
			# 	cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-run-dialog \"['<Primary><Shift>Space','<Primary>Space']\"")
			cmdline("gsettings set org.gnome.shell.keybindings toggle-application-view \"['LaunchB']\"")
			if dename != "mate":
				cmdline("gsettings set org.gnome.mutter overlay-key ''")
		if (distro == "ubuntu" and dename == "gnome") or (distro == "ubuntu" and dename == "budgie") or (distro == "linux" and dename == "mate") or (distro == "ubuntu" and dename == "mate"):
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up \"['<Super>Up','<Super>Left']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down \"['<Super>Down','<Super>Right']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings reset org.gnome.desktop.wm.keybindings panel-main-menu")
			# cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
		elif distro == "pop!_os" and dename == "gnome":
			cmdline("gsettings set org.gnome.desktop.wm.keybindings close \"['<Alt>F4','<Super>w']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings toggle-maximized \"['<Alt>F10','<Primary><Super>Up']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings reset org.gnome.desktop.wm.keybindings panel-main-menu")
			# cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up \"['<Super>Up','<Super>Left']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down \"['<Super>Down','<Super>Right']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ['']")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ['']")
		elif distro == "elementary" and dename == "gnome":
			if(kintotype == 1):
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>Tools','<Alt>Tab']\"")
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary><Shift>Tools','<Alt><Shift>Tab']\"")
			else:
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications \"['<Primary>F13','<Primary><Shift>F13','<Alt>Tab']\"")
				cmdline("gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward \"['<Primary>F14','<Primary><Shift>F14','<Alt><Shift>Tab']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings show-desktop \"['<Super>d','<Super>Down']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings toggle-maximized \"['<Alt>F10','<Super>Up']\"")
			cmdline("gsettings reset org.gnome.desktop.wm.keybindings panel-main-menu")
			# cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Control><Shift>Space','<Super>Space']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\"")
			cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Super>Space','<Primary>Space']\"")
			if(kintotype == 2):
				cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Elementary cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_term')
				cmdline('perl -pi -e "s/(\w.*)(\/\/ Default cmdtab)/\/\/ \$1\$2/g" ~/.xkb/symbols/mac_term')
				cmdline('perl -pi -e "s/(\/\/ )(.*)(\/\/ Elementary cmdtab)/\$2\$3/g" ~/.xkb/symbols/mac_gui')
				cmdline('perl -pi -e "s/(\w.*)(\/\/ Default cmdtab)/\/\/ \$1\$2/g" ~/.xkb/symbols/mac_gui')
		# elif distro == "budgie" and dename == "gnome":
		# 	print("Apply budgie shortcuts here")
		elif (dename == "xfce"):
			print("Applying xfce shortcuts...")
			cmdline('cp ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml ./xfce4-keyboard-shortcuts_`date +"%Y.%m.%d-%s"`.xml')
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
			# cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary>space" --create --type string --set "xfce4-popup-whiskermenu"')
			# cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary><Shift>space" --create --type string --set "xfce4-popup-whiskermenu"')
			cmdline('xfconf-query --reset --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary>space"')
			cmdline('xfconf-query --reset --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary><Shift>space"')
			cmdline('xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/default/<Primary>Escape" --create --type string --set "xfce4-popup-whiskermenu"')
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
			# cmdline("gsettings set org.gnome.desktop.wm.keybindings panel-main-menu \"['<Primary><Shift>Space','<Primary>Space']\"")
			cmdline("gsettings reset org.gnome.desktop.wm.keybindings panel-main-menu")
			cmdline("gsettings set org.gnome.mutter.keybindings toggle-tiled-right \"['<Super><Alt>Right']\"")
			cmdline("gsettings set org.gnome.mutter.keybindings toggle-tiled-left \"['<Super><Alt>Left']\"")
			# org.gnome.mutter.keybindings toggle-tiled-right ['<Super>Right']
			# org.gnome.mutter.keybindings toggle-tiled-left ['<Super>Left']
		elif dename == "kde":
			# cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "krunner.desktop" --key "_launch","Alt+Space\tAlt+F2\tSearch,Alt+Space\tAlt+F2\tSearch,KRunner"')
			# Remove Alt+F3 Operations Menu - Sublimetext Select-All
			cmdline('cp ~/.config/kwinrc ./kwinrc_`date +"%Y.%m.%d-%s"`')
			cmdline('cp ~/.config/kglobalshortcutsrc ./kde_kglobalshortcutsrc_`date +"%Y.%m.%d-%s"`')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Switch to Previous Desktop" "Meta+Left,Meta+Left,Switch to Previous Desktop"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Operations Menu" "none,Alt+F3,Window Operations Menu"')
			if(kintotype == 1):
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows" "Ctrl+Tools,Alt+Tab,Walk Through Windows"')
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows (Reverse)" "Ctrl+Shift+Tools,Alt+Shift+Backtab,Walk Through Windows (Reverse)"')
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows of Current Application" "Alt+F6,none,Walk Through Windows of Current Application"')
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows of Current Application (Reverse)" "Alt+Shift+F6,none,Walk Through Windows of Current Application (Reverse)"')
			else:
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows" "Ctrl+F13,Alt+Tab,Walk Through Windows"')
				cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows (Reverse)" "Ctrl+Shift+F14,Alt+Shift+Backtab,Walk Through Windows (Reverse)"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Walk Through Windows Alternative" "none,none,Walk Through Windows"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Maximize Window" "none,Meta+PgUp,Maximize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Maximize" "Meta+Ctrl+F,Alt+F10,Maximize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Minimize Window" "Meta+h,Meta+PgDown,Minimize Window"')
			cmdline('kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Switch to Next Desktop" "Meta+Right,Meta+Right,Switch to Next Desktop"')
			os.system('kquitapp5 kglobalaccel && sleep 2s && kglobalaccel5 &')
		else:
			print('distro: ' + distro + ' de: ' + dename)
			print(bcolors.CRED2 + "A supported OS and DE was not found, you may not have full system level shortcuts installed." + bcolors.ENDC)
			print(bcolors.CRED2 + "You may want to find your DE or Window Manager settings and manually set Alt-Tab & other OS related shortcuts." + bcolors.ENDC)
		if dename == "gnome" or dename == "mate" or dename == "budgie":
			# Apply dconf update to make updates survive reboots
			cmdline('dconf dump /org/gnome/desktop/wm/keybindings/ > tempkb.conf')
			cmdline('dconf dump /org/gnome/mutter/keybindings/ > tempmt.conf')
			cmdline('dconf load /org/gnome/desktop/wm/keybindings/ < tempkb.conf')
			cmdline('dconf load /org/gnome/mutter/keybindings/ < tempmt.conf')
			cmdline('sleep 1 && rm -f ./tempkb.conf;rm -f ./tempmt.conf')
			if dename == "budgie":
				print('** Make sure to open Keyboard settings & reset "switch applications" to cmd+tab **')
			# cmdline('dconf update')

def Uninstall():
	print("You selected to Uninstall Kinto.\n")
	restore = yn_choice("\nYour DE is " + dename + ".\n\nY: Restore hotkeys from backup\nN: Reset OS/DE hotkeys\nWhich option would you prefer?")
	print("")
	if(restore):
		if dename == "gnome":
			print("Restoring DE hotkeys...")
			wmkeys = cmdline('ls | grep -m1 "keybinding"')
			mutterkeys = cmdline('ls | grep -m1 "mutter_"')
			if len(wmkeys) > 0:
				print('dconf load /org/gnome/desktop/wm/keybindings/ < ' + wmkeys)
				cmdline('dconf load /org/gnome/desktop/wm/keybindings/ < ' + wmkeys)
			else:
				print('Gnome Desktop keybindings backup not found...')
			if len(mutterkeys) > 0:
				print('dconf load /org/gnome/mutter/keybindings/ < ' + mutterkeys)
				cmdline('dconf load /org/gnome/mutter/keybindings/ < ' + mutterkeys)
			if len(wmkeys) > 0 or len(mutterkeys) > 0:
				print("Gnome hotkeys have been successfully restored.")
		elif dename == "kde":
			print("Restoring DE hotkeys...")
			kwinkeys = cmdline('ls | grep -m1 "kwinrc"').strip()
			kdekeys = cmdline('ls | grep -m1 "kglobalshortcutsrc"').strip()
			cmdline('cp ./' + kdekeys + ' ~/.config/kglobalshortcutsrc')
			cmdline('cp ./' + kwinkeys + ' ~/.config/kwinrc')
		elif dename == "xfce":
			print("Restoring DE hotkeys...")
			xfcekeys = cmdline('ls | grep -m1 "xfce4-keyboard"').strip()
			cmdline('cp ./' + xfcekeys + ' ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml')
		if dename == "gnome" or dename == "kde" or dename == "xfce":
			print("./uninstall.sh\n")
			subprocess.check_call(shlex.split("./uninstall.sh"))
			print("Done.")
		if dename == "kde" or dename == "xfce":
			print("Please log off and back on for your original hotkeys to take effect.")
	else:
		if dename == "gnome":
			print("Resetting DE hotkeys...\n")
			print("gsettings reset-recursively org.gnome.desktop.wm.keybindings")
			cmdline("gsettings reset-recursively org.gnome.desktop.wm.keybindings")
			print("gsettings reset-recursively org.gnome.mutter.keybindings")
			cmdline("gsettings reset-recursively org.gnome.mutter.keybindings")
			print("gsettings set org.gnome.mutter overlay-key 'super'")
			cmdline("gsettings set org.gnome.mutter overlay-key 'super'")
			cmdline('dconf dump /org/gnome/mutter/ > mutter.conf')
			cmdline('dconf load /org/gnome/mutter/ < mutter.conf')
		elif dename == "kde":
			print("Resetting DE hotkeys...\n")
			cmdline('mv ~/.config/kwinrc ~/.config/kwinrc.kinto')
			cmdline('mv ~/.config/kglobalshortcutsrc ~/.config/kglobalshortcutsrc.kinto')
		elif dename == "xfce":
			print("Resetting DE hotkeys...\n")
			cmdline('cp /etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml')
		if dename == "gnome" or dename == "kde" or dename == "xfce":
			print("./uninstall.sh\n")
			subprocess.check_call(shlex.split("./uninstall.sh"))
			print("Done.")
		if dename == "kde" or dename == "xfce":
			print("Please log off and back on for your original DE hotkeys to take effect.")

def kintoImpOne():

	check_xbind = cmdline("\\which xbindkeys 2>/dev/null").strip()
	check_xdotool = cmdline("\\which xdotool 2>/dev/null").strip()
	check_ibus = cmdline("\\which ibus-setup 2>/dev/null").strip()

	pkgm = cmdline("\\which apt-get 2>/dev/null").strip()

	if len(pkgm) == 0:
		pkgm = cmdline("\\which dnf 2>/dev/null").strip()
		if len(pkgm) > 0:
			pkgm += " check-update;sudo dnf install -y "
	else:
		pkgm += " install -y "
		pkgm += " update; sudo apt-get install -y "

	if len(pkgm) == 0:
		pkgm = cmdline("\\which pacman 2>/dev/null").strip()
		if len(pkgm) > 0:
			pkgm += " -Syy; sudo pacman -S "


	if len(pkgm) == 0:
		print("No supported package manager found. Exiting...")
		sys.exit()


	runpkg = 0
	global run_pkg

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
		print(runpkg)
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

with open('defaults.json') as json_file:
	data = json.load(json_file)


color_arr = [bcolors.CBEIGE,bcolors.CRED2,bcolors.CGREEN,bcolors.CYELLOW ]

print("\nKinto - Type in Linux like it's a Mac.\n")

kintotype = int(input(color_arr[2] +
	"1) Kinto - xkeysnail (udev/x11) - Recommended\n" + color_arr[0] +
	"2) Kinto - Original xkb/x11 implementation\n" + color_arr[3] +
	"3) Uninstall Kinto - xkeysnail\n" +
	"4) Uninstall Kinto - Original xkb\n\n"
	+ bcolors.ENDC))
print("")
if(kintotype == 1):
	subprocess.check_call(shlex.split("./xkeysnail_service.sh"))
	if os.path.isdir(homedir + "/.config/kinto") == True:
		setShortcuts()
		subprocess.check_call(shlex.split("./xkeysnail_service.sh budgieUpdate"))
	exit()

if(kintotype == 3):
	subprocess.check_call(shlex.split("./xkeysnail_service.sh uninstall"))
	exit()

if(kintotype == 4):
	Uninstall()
	exit()

kintoImpOne()

for index, item in enumerate(data['defaulttypes']):
	ossym = ""
	if item == "windows":
		ossym = u'\u2756'
	elif item == "mac":
		ossym = u'\u2318'
	elif item == "chromebook":
		ossym = u'\u2707'
	print("%s    %i. %s  %s %s" % (color_arr[index], index+1, ossym, item.capitalize(), bcolors.ENDC))

print("%s    %i. Uninstall %s" % (color_arr[3], len(data['defaulttypes'])+1, bcolors.ENDC))

default = 0
while not int(default) in range(1,len(data['defaulttypes'])+2):
	default = int(input(bcolors.CYELLOW2 + "\nPlease enter your keyboard type (1 - " + str(len(data['defaulttypes'])) + ") : " + bcolors.ENDC))
print("")

if default == len(data['defaulttypes'])+1:
	Uninstall()
	exit()

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

keyboardconfigs = [obj for obj in data['defaults'] if(obj['type'] == data['defaulttypes'][default-1])]

# for k in keyboardconfigs:
for index, k in enumerate(keyboardconfigs):
	print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
	print(bcolors.CYELLOW2 + 'Description: ' + k['description'] + bcolors.ENDC)

print("")
defaultkb = 0
while not int(defaultkb) in range(1,len(keyboardconfigs)+1):
	defaultkb = int(input(bcolors.CYELLOW2 + "Please enter your keyboard config (1 - " + str(len(keyboardconfigs)) + ") : " + bcolors.ENDC))
print("")

if 'hack' in keyboardconfigs[defaultkb-1]:
	print(bcolors.CYELLOW2 + "You have selected a keyboard config that needs the following command to be ran.\n" + bcolors.ENDC)
	print(keyboardconfigs[defaultkb-1]['hack'].replace(";", "\n") + "\n")
	runhack = yn_choice(bcolors.CYELLOW2 + "Would you like to run it now? (Will require sudo privileges. Will exit on No.)" + bcolors.ENDC)
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
		print(bcolors.CYELLOW2 + 'Description: ' + k['description'] + bcolors.ENDC)
		print(bcolors.CYELLOW2 + 'run: ' + k['run'].replace(";", "\n") + bcolors.ENDC + '\n')

	print(bcolors.CYELLOW2 + "Please enter your init tweak(s) (eg 1 or 1 2 3 - leave blank to skip): " + bcolors.ENDC)
	defaultinit = [int(i) for i in input().split()]
	if len(defaultinit) != 0:
		user_config['init'] = [intents[defaultinit[0]-1]['id']]

print("\nDynamic shortcut tweaks\n")

intents = [obj for obj in user_config['de'] if(obj['intent'] == "gui_term")]
tweaks = []
tweaks_selected = []

for index, k in enumerate(intents):
	print(color_arr[default-1] + bcolors.BOLD + str(index+1) + '. ' + k['name'] + bcolors.ENDC)
	print(bcolors.CYELLOW2 + 'Description: ' + k['description'] + bcolors.ENDC)
	print(bcolors.CYELLOW2 + 'run in gui mode: ' + k['run_gui'].replace(";", "\n") + bcolors.ENDC)
	print(bcolors.CYELLOW2 + 'run in terminal mode: ' + k['run_term'].replace(";", "\n") + bcolors.ENDC + '\n')
	tweaks.append(k['id'])

print(bcolors.CYELLOW2 + "Please enter your dynamic shortcut tweak(s) (eg 1 or 1 2 3 - leave blank to skip): " + bcolors.ENDC)
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