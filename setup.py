#!/usr/bin/env python3
import json, time, os, sys, subprocess, shlex, platform,argparse
from shutil import copyfile
from subprocess import PIPE, Popen
from prekinto import *

parser = argparse.ArgumentParser()

parser.add_argument('-r', dest='uninstall', action='store_true', help="uninstall kinto")
parser.add_argument('--remove', dest='uninstall', action='store_true', help="uninstall kinto")

args = parser.parse_args()

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
		os.system('copy /Y "' + path + '\\windows\\kinto.ahk" "' + homedir + '\\kinto-new.ahk"')
	if default < 3:
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Default)(?!( - ST2CODE))(.*)/$2$3$5/gm" ' + homedir + '\\kinto-new.ahk')
	if default == 1:
		kbtype = "mac"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; MacModifiers)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
	elif default == 2:
		kbtype = "win"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
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
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Chromebook)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers\/CB)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
	if default == 3 or default == 4:
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; CB\/IBM)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; WinModifiers\/CB\/IBM)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
	if default == 4:
		kbtype = "ibm"
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; IBM)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
	if default > 0 and default < 5:
		stvscode = yn_choice(bcolors.CYELLOW2 + "Would you like to use Sublime Text 3 keymaps in VS Code?\n" + bcolors.ENDC)
		print("\nWill now install Ubuntu Terminal Theme as default...")
		os.system('regedit "' + path + '\\windows\\theme_ubuntu.reg"')
		os.system('robocopy "'+ path + '\\assets" "%userprofile%\\.kinto\\assets" /E')
		if (stvscode and (default > 0 or default < 3)):
			os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; Default - ST2CODE)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
		elif (stvscode and (default == 3 or default == 4 )):
			os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/(; )(.*)(; CB/IBM - ST2CODE)/$2$3/gm" ' + homedir + '\\kinto-new.ahk')
		os.system('copy /Y "' + path + '\\windows\\kinto-start.vbs" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('C:\\Strawberry\\perl\\bin\\perl.exe -pi -e "s/{kbtype}/' + kbtype + '/gm" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('copy /Y "' + path + '\\windows\\usb.vbs" "%userprofile%\\.kinto\\usb.vbs"')
		os.system('copy /Y "' + path + '\\windows\\detectUSB.ahk" "%userprofile%\\.kinto\\detectUSB.ahk"')
		os.system('mklink "%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\STARTM~1\\Programs\\Startup\\kinto-start.vbs" "%userprofile%\\.kinto\\kinto-start.vbs"')
		os.system('copy /Y "'+ path + '\\windows\\NoShell.vbs" "%userprofile%\\.kinto\\NoShell.vbs"')
		os.system('copy /Y "'+ path + '\\windows\\toggle_kb.bat" "%userprofile%\\.kinto\\toggle_kb.bat"')
		os.system('copy /Y "'+ homedir + '\\kinto-new.ahk" "%userprofile%\\.kinto\\kinto.ahk"')
		os.system("del /f " + homedir + "\\kinto-new.ahk")
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
dename = cmdline("./linux/system-config/dename.sh").replace('"','').strip().split(" ")[0].lower()

run_pkg = ""

if os.path.isdir(homedir + "/.config/kinto") == False:
	os.mkdir(homedir + "/.config/kinto")
	time.sleep(0.5)


cmdline("git fetch")

color_arr = [bcolors.CBEIGE,bcolors.CRED2,bcolors.CGREEN,bcolors.CYELLOW ]

kintover = cmdline('echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)"')

print("\nKinto " + kintover + "Type in Linux like it's a Mac.\n")

if args.uninstall:
	subprocess.check_call(shlex.split("./xkeysnail_service.sh uninstall"))
	exit()

subprocess.check_call(shlex.split("./xkeysnail_service.sh"))


