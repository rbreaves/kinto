#!/bin/bash

# set about:config?filter=ui.key.menuAccessKeyFocuses
# to false for wordwise to work in Firefox

function pause(){
 read -s -n 1 -p "Press any key to continue . . ."
 echo ""
}

typeset -l distro
distro=$(awk -F= '$1=="NAME" { gsub("[\",!,_, ]","",$2);print $2 ;}' /etc/os-release)
typeset -l dename
dename=$(./linux/system-config/dename.sh | cut -d " " -f1)

sysv=$(pidof systemd >/dev/null 2>&1 && echo "1" || echo "0")

function uninstall {

	echo -e "\nNote: Restoring keys is only relevant if you had installed a version prior to 1.2 of Kinto. You should skip this step if 1.2+ is all you have installed."

	while true; do
	read -rep $'\nPress R to restore your original shortcuts.\nPress F to reset to factory shortcuts.\nPress N to skip. (f/r/N)\n' yn
		case $yn in
			[Ff]* ) yn="f"; break;;
			[Rr]* ) yn="r";break;;
			[Nn]* ) yn="n";break;;
			* ) yn="n";break;;
		esac
	done

	if [ "$yn" == "f" ];then
		echo "Reset to factory shortcuts"
		if [[ $dename == "gnome" || $dename == "budgie" ]];then
			echo "Resetting DE hotkeys..."
			echo "gsettings reset-recursively org.gnome.desktop.wm.keybindings"
			gsettings reset-recursively org.gnome.desktop.wm.keybindings
			echo "gsettings reset-recursively org.gnome.mutter.keybindings"
			gsettings reset-recursively org.gnome.mutter.keybindings
			dconf dump /org/gnome/mutter/ > mutter.conf
			dconf load /org/gnome/mutter/ < mutter.conf
		elif [ "$dename" == "kde" ];then
			echo "Resetting DE hotkeys..."
			mv ~/.config/kwinrc ~/.config/kwinrc.kinto
			mv ~/.config/kglobalshortcutsrc ~/.config/kglobalshortcutsrc.kinto
		elif [ "$dename" == "xfce" ];then
			echo "Resetting DE hotkeys..."
			if test -f "/etc/mx-version";then
				cp /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
			else
				cp /etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
			fi
		fi
	elif [ "$yn" == "r" ]; then
		echo "Restore original user shortcuts"
		if [[ $dename == "gnome" || $dename == "budgie" ]]; then
			echo "Restoring DE hotkeys..."
			wmkeys=$(ls | grep -m1 "keybinding")
			mutterkeys=$(ls | grep -m1 "mutter_")
			if [[ ${#wmkeys} > 0 ]]; then
				echo "dconf load /org/gnome/desktop/wm/keybindings/ < $wmkeys"
				dconf load /org/gnome/desktop/wm/keybindings/ < "$wmkeys"
			else
				echo "Gnome Desktop keybindings backup not found..."
			fi
			if [[ ${#mutterkeys} > 0 ]]; then
				echo "dconf load /org/gnome/mutter/keybindings/ < $mutterkeys"
				dconf load /org/gnome/mutter/keybindings/ <"$mutterkeys"
			fi
			if [[ ${#wmkeys} > 0 ]] || [[ ${#mutterkeys} > 0 ]]; then
				echo "Gnome hotkeys have been successfully restored."
			fi
		elif [ "$dename" == "kde" ]; then
			echo "Restoring DE hotkeys..."
			kwinkeys=$(ls | grep -m1 "kwinrc")
			kdekeys=$(ls | grep -m1 "kglobalshortcutsrc")
			cp ./"$kdekeys" ~/.config/kglobalshortcutsrc
			cp ./"$kwinkeys" ~/.config/kwinrc
		elif [ "$dename" == "xfce" ]; then
			echo "Restoring DE hotkeys..."
			xfcekeys=$(ls | grep -m1 "xfce4-keyboard")
			cp ./"$xfcekeys" ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
		fi
	elif [ "$yn" == "n" ]; then
		echo "Skipping..."
	fi
	if [[ $dename == "gnome" || $dename == "budgie" || $dename == "mate" ]]; then
		echo -e "\nWill still be restoring the overlay key"
		echo -e "gsettings set org.gnome.mutter overlay-key 'super'\n"
		gsettings set org.gnome.mutter overlay-key 'super'
	# Repetitive - xfce restore factory or backup does this
	# Also needs to check if whiskermenu is even being used
	# elif [[ $dename == "xfce" ]]; then
	# 	echo -e "\nWill still be restoring the overlay key"
	# 	echo -e "xfconf-query --channel xfce4-keyboard-shortcuts --property \"/commands/custom/Super_L\" --create --type string --set \"xfce4-popup-whiskermenu\""
	# 	xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/Super_L" --create --type string --set "xfce4-popup-whiskermenu"
	fi
}

function removeAppleKB {
	# Undo Apple keyboard cmd & alt swap
	if test -f "/sys/module/hid_apple/parameters/swap_opt_cmd" && [ `cat /sys/module/hid_apple/parameters/swap_opt_cmd` == "1" ]; then
		echo '0' | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd
		echo 'options hid_apple swap_opt_cmd=0' | sudo tee /etc/modprobe.d/hid_apple.conf
		sudo update-initramfs -u -k all
	fi
	if test -f "/sys/module/applespi/parameters/swap_opt_cmd" && [ `cat /sys/module/applespi/parameters/swap_opt_cmd` == "1" ]; then
		echo '0' | sudo tee /sys/module/applespi/parameters/swap_opt_cmd
		echo 'options applespi swap_opt_cmd=0' | sudo tee /etc/modprobe.d/applespi.conf
		sudo update-initramfs -u -k all
	fi
}

function budgieUninstall {
	if [ -f /usr/bin/budgie-desktop ];then
		echo -e "\nYour system may log you off immediately during the restoration of budgie-daemon.\n"
		read -n 1 -s -r -p "Press any key to continue..."
		bdmd5="$(md5sum /usr/bin/budgie-daemon | awk '{ print $1 }')"
		oldbdmd5=$(md5sum ./budgie-daemon_10.5.1.bak | awk '{ print $1 }')
		if [ "$bdmd5" != "$oldbdmd5" ]; then
			echo -e "\nReplacing budgie-daemon with backup..."
			sudo pkill budgie-daemon && sudo cp ./budgie-daemon_10.5.1.bak /usr/bin/budgie-daemon
		else
			echo -e "\nBudgie-daemon is already an original."
		fi
	fi
}

function budgieUpdate {
	# Check for budgie and install App Switching hack
	if [ -f /usr/bin/budgie-desktop ];then
		while true; do
			read -rep $'Would you like to update Budgie to support proper App Switching? (y/n)\n(Your system may immediately log you out after this runs.)\n' yn
			case $yn in
				[Yy]* ) yn="y"; break;;
				[Nn]* ) yn="n";break;;
				* ) echo "Please answer yes or no.";;
			esac
		done
		if [ "$yn" == "y" ]; then
			budgieVersion="$(/usr/bin/budgie-desktop --version | awk '{ print $2; }' | head -n1)"
			if [ "$budgieVersion" == "10.5.1" ]; then
				if ! [ -f ./linux/system-config/budgie-daemon_10.5.1 ]; then
					wget https://github.com/rbreaves/budgie-desktop/blob/binaries/binaries/budgie-daemon_10.5.1?raw=true -O ./linux/system-config/budgie-daemon_10.5.1
				fi
				bdmd5=$(md5sum /usr/bin/budgie-daemon | awk '{ print $1 }')
				newbdmd5=$(md5sum ./linux/system-config/budgie-daemon_10.5.1 | awk '{ print $1 }')
				if [ "$bdmd5" != "$newbdmd5" ]; then
					cp /usr/bin/budgie-daemon ./budgie-daemon_"$budgieVersion".bak
					sudo pkill budgie-daemon && sudo cp ./linux/system-config/budgie-daemon_10.5.1 /usr/bin/budgie-daemon
					echo "Updated Budgie to use App Switching Patch"
				else
					echo "Budgie-daemon already patched, skipping replacement."
				fi
			else
				echo "Your Budgie version was $budgieVersion and the patch is for 10.5.1."
				while true; do
					read -rep $'Would you like to replace it any ways? (y/n)\n(A backup will be made)\n' yn
					case $yn in
						[Yy]* ) yn="y"; break;;
						[Nn]* ) yn="n";break;;
						* ) echo "Please answer yes or no.";;
					esac
				done
				if [ "$yn" == "y" ]; then
					if ! [ -f ./linux/system-config/budgie-daemon_10.5.1 ]; then
						wget https://github.com/rbreaves/budgie-desktop/raw/43d3b44243b0bcaee3262a79818024a651475b58/binaries/budgie-daemon_10.5.1 -O ./linux/system-config/budgie-daemon_10.5.1
					fi
					cp /usr/bin/budgie-daemon ./budgie-daemon_"$budgieVersion".bak
					sudo pkill budgie-daemon && sudo cp ./linux/system-config/budgie-daemon_10.5.1 /usr/bin/budgie-daemon
					echo "Updated Budgie to use App Switching Patch"
				fi
			fi
		fi
	fi
}

if [[ $1 == "5" || $1 == "uninstall" || $1 == "Uninstall" ]]; then
	echo "Uninstalling Kinto - xkeysnail (udev)"
	uninstall
	echo "Removing any Apple driver settings Kinto may have have set..."
	removeAppleKB
	echo "Killing the Kinto tray..."
	pkill -f kintotray >/dev/null 2>&1
	echo "Stopping the Kinto service..."
	sudo systemctl stop xkeysnail >/dev/null 2>&1
	echo "Disabling the Kinto service..."
	sudo systemctl disable xkeysnail >/dev/null 2>&1
	echo "Killing any remaining xkeysnail processes..."
	sudo pkill -f bin/xkeysnail >/dev/null 2>&1
	echo "Killing any Kinto related threads from Kinto tray or the gui..."
	sudo pkill -f "is-active xkeysnail" >/dev/null 2>&1
	echo -e "\nRemoving Kinto..."
	echo "rm /etc/sudoers.d/limitedadmins"
	echo "rm ~/.config/autostart/xkeysnail.desktop"
	echo "rm ~/.config/autostart/kintotray.desktop"
	echo "rm -rf ~/.config/kinto"
	echo "rm /usr/share/applications/kinto.desktop"
	sudo rm /etc/sudoers.d/limitedadmins >/dev/null 2>&1
	rm ~/.config/autostart/xkeysnail.desktop >/dev/null 2>&1
	rm ~/.config/autostart/kintotray.desktop  >/dev/null 2>&1
	rm -rf ~/.config/kinto >/dev/null 2>&1
	sudo rm /usr/share/applications/kinto.desktop  >/dev/null 2>&1
	echo -e "\nRemoving Kinto's systemd service files..."
	echo "rm /etc/systemd/system/xkeysnail.service"
	echo "rm /etc/systemd/system/graphical.target.wants/xkeysnail.service"
	echo "rm /usr/lib/systemd/system/xkeysnail.service"
	echo "rm /lib/systemd/system/xkeysnail.service"
	sudo rm /etc/init.d/kinto >/dev/null 2>&1
	sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	sudo rm /etc/systemd/system/graphical.target.wants/xkeysnail.service >/dev/null 2>&1
	sudo rm /usr/lib/systemd/system/xkeysnail.service >/dev/null 2>&1
	sudo rm /lib/systemd/system/xkeysnail.service >/dev/null 2>&1
	if [ -f /usr/local/bin/logoff.sh ];then
		sudo rm /usr/local/bin/logoff.sh
	fi
	if [[ $distro == "elementaryos" ]]; then
		gsettings set io.elementary.terminal.settings natural-copy-paste true
	fi
	sudo systemctl daemon-reload
	# sudo systemctl --state=not-found --all | grep xkeysnail
	exit 0
fi

sudo systemctl stop xkeysnail >/dev/null 2>&1
sudo systemctl disable xkeysnail >/dev/null 2>&1
sudo pkill -f bin/xkeysnail >/dev/null 2>&1
sudo pkill -f kinto-gui.py >/dev/null 2>&1
sudo pkill -f kintotray.py >/dev/null 2>&1
ps aux | awk '/[s]h -c while/ {print $2}' | xargs -r -n1 sudo kill
sudo pkill -f "is-active xkeysnail" >/dev/null 2>&1

if [ "$distro" == "manjarolinux" ]; then
	while true; do
		read -rep $'\nHave you run \"sudo pacman -Syu\" before running Kinto setup? (y/n): ' updated	
		case $updated in
			[Yy]* ) mjupdated='yes'; break;;
			[Nn]* ) mjupdated='no'; break;;
			* ) echo -e "\nPlease answer [y]es or [n]o.";;
		esac
	done
	if [[ "$mjupdated" == "no" ]]; then 
		echo 
		echo "================================================================================"
		echo "==========  Please run a full system update before installing Kinto.  ==========" 
		echo "================================================================================"
		echo 
		exit 0
	fi
fi

# Add additional shortcuts if needed, does not modify existing ones

if [[ $dename == 'gnome' || $dename == 'budgie' ]];then
	if [[ $(gsettings get org.gnome.mutter overlay-key | grep "''\|' '" | wc -l) != 1 ]];then
		bound=$(gsettings get org.gnome.mutter overlay-key)
		echo "Overlay key, " $bound ", detected. Will be removing so Super-Space can remap to Cmd-Space for app launching.."
		gsettings set org.gnome.mutter overlay-key ''
	fi
elif [[ $dename == 'xfce' ]];then
	launcher=$(cat ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml | grep 'name="Super_L"' | sed 's:.*="::')
	# echo "${#launcher}"
	if [[ "${#launcher}" -eq 0 ]]; then
		xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/Super_L" --create --type string --set "xfce4-popup-whiskermenu"
		echo "Resetting Super_L, please wait..."
		sleep 6
		launcher=$(cat ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml | grep 'name="Super_L"' | sed 's:.*="::')
		if [[ "${#launcher}" -gt 0 ]]; then
			echo "Success."
		else
			echo "Failed. Skipping setup of Cmd-Space."
		fi
	fi
	if [[ "${#launcher}" -gt 0 ]]; then
		nlauncher=${launcher::-3}
		# Replace Alt-F1 help file w/ whisker menu alternative hotkey
		xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Alt>F1" --reset
		# Clear Alt-F3 App Finder for sublime text global replace
		xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Alt>F3" --reset
		xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Alt>F1" --create --type string --set "$nlauncher" && echo "$nlauncher has been set to Alt-F1 for Cmd-Space to work."
		# Unset Super_L to avoid issues during setup, will re-apply at the end
		xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/Super_L" --reset
		# xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Super>grave" --create --type string --set "switch_window_key"

	fi
	# Unset Super-Tab, breaks Ctrl-Tab. switch_window_key
	sed -i '/.*name=\"&lt;Super&gt;Tab.*$/d' ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
fi

# if ls /etc/apt/sources.list.d/system76* 1> /dev/null 2>&1; then
if [[ $distro == 'popos' ]]; then
	# Addition, does not overwrite existing
	if [[ $(gsettings get org.gnome.desktop.wm.keybindings minimize | grep "\[\]" | wc -l) != 1 ]];then
		echo "Adding Super-h (Cmd+h) to hide/minimize Window."
		gsettings set org.gnome.desktop.wm.keybindings minimize "['<Super>h','<Alt>F9']"
		# work around to make sure settings survive reboot
		dconf dump /org/gnome/desktop/wm/keybindings/ > tempkb.conf
		dconf load /org/gnome/desktop/wm/keybindings/ < tempkb.conf
	else
		bound=$(gsettings get org.gnome.desktop.wm.keybindings minimize)
		echo "Hide/minimize Window is already bound to " $bound " , please remap it to Super-H for kinto."
		echo "gsettings set org.gnome.desktop.wm.keybindings minimize \"['<Super>h','<Alt>F9']\""
	fi
fi

if [[ $distro == "elementaryos" ]]; then
	gsettings set io.elementary.terminal.settings natural-copy-paste false
	sudo ./linux/system-config/unipkg.sh libvte-2.91-dev
fi

if ! [ -x "$(command -v xhost)" ] || ! [ -x "$(command -v gcc)" ]; then
	if [ "$distro" == "manjarolinux" ]; then
		sudo ./linux/system-config/unipkg.sh "xorg-xhost gcc"
	fi
fi

if [[ $dename == "kde" ]]; then
	if [[ $distro == "manjarolinux" ]] || cat /etc/os-release | grep -E "^ID(_LIKE)?" | grep -q arch; then # Manjario or other arch-like distros: SteamOS3,HoloISO
		sudo ./linux/system-config/unipkg.sh vte3
		sudo ./linux/system-config/unipkg.sh python-pip
	else
		sudo ./linux/system-config/unipkg.sh libvte-2.91-dev
	fi
fi
if [[ $distro == 'kdeneon' ]]; then
	kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Show Desktop" "Meta+D,none,Show Desktop"
	kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Close" "Alt+F4,none,Close Window"
	kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Minimize" "Meta+PgDown,none,Minimize Window"
	kwriteconfig5 --file "$HOME/.config/kglobalshortcutsrc" --group "kwin" --key "Window Maximize" "Meta+PgUp,none,Maximize Window"
	kquitapp5 kglobalaccel && sleep 2s && kglobalaccel5 &
fi

if [[ $distro == 'fedora' ]] || [[ $distro == 'fedoralinux' ]]; then
	if [[ $(gsettings get org.gnome.desktop.wm.keybindings show-desktop | grep "\[\]" | wc -l) == 1 ]];then
		gsettings set org.gnome.desktop.wm.keybindings show-desktop "['<Super>d']"
	else
		if [[ $(gsettings get org.gnome.desktop.wm.keybindings show-desktop | grep "<Super>d" | wc -l) == 0 ]]; then
			echo 'Kinto will not set your "Show Desktop" hotkey due to it already being set.\nPlease set Show Desktop to Super-D, or Edit Kinto'"'"'s config.'
			echo "Did not run the following."
			echo "gsettings set org.gnome.desktop.wm.keybindings show-desktop \"['<Super>d']\""	
		fi
	fi
fi

# if [ $# -eq 0 ]; then
# 	echo "Install Kinto - xkeysnail (udev)"
# 	echo "  1) Windows & Mac (HID driver) - Most Standard keyboards (& 1st party usb/bt Apple keyboards)"
# 	echo "  2) Mac Only & VMs on Macbooks - 3rd & 1st party Apple keyboards"
# 	echo "  3) Chromebook - Chromebook running Linux"
# 	echo "  4) IBM M - Keyboards w/o Super/Win keys"
# 	# echo "  5) Uninstall"

# 	read n

# 	set "$n"
# fi

# branch=$(git rev-parse --abbrev-ref HEAD)
# if [ "$branch" == "dev" ] || [ "$branch" == "alpha" ];then
# 	while true; do
# 	read -rep $'\nExperimental Support for Firefox/Chrome Back/Forward hotkeys (Cmd+Left/Right)?\n(Keys could get stuck, switch windows or press ctrl &/or super to release) (y/n)\n' yn
# 	case $yn in
# 		[Yy]* ) exp='/sbin/runuser -l {username} -c "export DISPLAY={displayid};{homedir}/.config/kinto/caret_status_xkey.sh\&";'; expsh='"{homedir}/.config/kinto/caret_status_xkey.sh"'; break;;
# 		[Nn]* ) exp=" "; expsh=" " break;;
# 		# * ) echo "Please answer yes or no.";;
# 	esac
# 	done
# else
# 	echo -e "\nSupport for Firefox/Chrome Back/Forward hotkeys (Cmd+Left/Right) disabled on $branch w/ xkeysnail \n"
exp=" "
expsh=" "
# fi
# sudo systemctl enable xkeysnail >/dev/null 2>&1
# if ! [ -x "$(command -v inotifywait)" ]; then
# 	echo "Will need to install inotify-tools to restart key remapper live for config file changes..."
# 	sudo ./linux/system-config/unipkg.sh inotify-tools
# fi
if ! [ -x "$(command -v git)" ]; then
	echo "Will need to install git..."
	sudo ./linux/system-config/unipkg.sh git
fi
if ! [ -x "$(command -v pip3)" ]; then
	echo "Will need to install python3-pip..."
	sudo ./linux/system-config/unipkg.sh python3-pip
fi
if ! [ -x "$(command -v python3-config)" ]; then
	if [ "$distro" == "ubuntu" ] || [ "${distro::6}" == "debian" ] || [ "$distro" == 'linuxmint' ]; then
		pydev="python3-dev python3-tk"
	elif [ "$distro" == "fedora" ] || [ "$distro" == "fedoralinux" ]; then
		pydev="python3-devel python3-tkinter"
	fi
	if [ "$distro" == "gnome" ] || [ "$distro" == "fedora" ] || [ "$distro" == "fedoralinux" ] || [ "${distro::6}" == "debian" ] || [ "$distro" == 'linuxmint' ] ; then
		echo "Will need to install $pydev..."
		sudo ./linux/system-config/unipkg.sh "$pydev"
	fi
fi
# if [ "$distro" == "ubuntu" ] && [ "$dename" == "gnome" ];then
# 	sudo ./linux/system-config/unipkg.sh gnome-tweaks gnome-shell-extension-appindicator gir1.2-appindicator3-0.1
# fi
if ! [ -x "$(command -v xhost)" ] || ! [ -x "$(command -v gcc)" ]; then
	if [ "$distro" == "\"manjaro linux\"" ]; then
		sudo ./linux/system-config/unipkg.sh "xorg-xhost gcc"
	fi
fi
if [ "$distro" == 'linuxmint' ] ; then
	pip3 install setuptools
elif [ "${distro::6}" == "debian" ]; then
	sudo pip3 install setuptools wheel
fi

pip3 install pillow

# echo "Transferring files..."
mkdir -p ~/.config/kinto

# KDE xhost fix
# mkdir -p ~/.kde/Autostart
# echo -e '#!/bin/sh\rxhost +SI:localuser:root' > ~/.kde/Autostart/kintohost.sh
# chmod +x ~/.kde/Autostart/kintohost.sh

# KDE startup - xhost fix
mkdir -p ~/.config/autostart
if [ ! "$sysv" -eq 0 ];then
	yes | cp -rf ./linux/xkeysnail.desktop ~/.config/kinto/xkeysnail.desktop
else
	yes | cp -rf ./linux/xkeysnail_sysv.desktop ~/.config/kinto/xkeysnail.desktop
fi

# yes | cp -rf ./linux/xkeystart.sh ~/.config/kinto/xkeystart.sh

# *** More testing needing, universal way of killing kinto on user log out? ***
# yes | sudo cp -rf linux/root_logoff.sh /usr/local/bin/logoff.sh
# sudo chown root:root /usr/local/bin/logoff.sh
# sudo chmod u+rwx /usr/local/bin/logoff.sh
# sudo chmod go-w+rx /usr/local/bin/logoff.sh
# *** End universal killing of kinto

# logoff fix - not solid for every os. Prevents missed 1 character input on login
# yes | sudo cp -rf linux/gnome_logoff.sh ~/.config/kinto/logoff.sh

if [ -d "./.git" ] 
then
	echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)" > ~/.config/kinto/version
elif [ -f "./dl_version" ]; then
	cp ./dl_version  ~/.config/kinto/version
else
	# Not a typo - v is built in
	echo "ersion Unknown"  > ~/.config/kinto/version
fi

yes | cp -rf ./linux/kinto.py ./linux/kinto.py.new
yes | cp -rf ./linux/gui/ ~/.config/kinto/
yes | cp -nrf ./linux/initkb ~/.config/kinto/initkb
yes | cp -rf ./linux/killdups.sh ~/.config/kinto/killdups.sh
yes | cp -rf ./linux/trayapps/appindicator/kintotray.py ~/.config/kinto/kintotray.py
yes | cp -rf ./linux/trayapps/appindicator/kintotray.desktop ~/.config/kinto/kintotray.desktop
yes | cp -rf ./linux/gui/kinto.desktop ./linux/gui/kinto.desktop.new
yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color.svg
yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color-48.svg
yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-invert-16.svg ~/.config/kinto/kinto-invert.svg
yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-solid-16.svg ~/.config/kinto/kinto-solid.svg
yes | cp -rf ./linux/trayapps/appindicator/icons/kinto.svg ~/.config/kinto/kinto.svg
# yes | cp -rf ./linux/system-config/caret_status_xkey.sh ~/.config/kinto/caret_status_xkey.sh

yes | cp -rf ./linux/limitedadmins ./linux/limitedadmins.new
sed -i "s/{username}/`whoami`/g" ./linux/limitedadmins.new
sed -i "s#{systemctl}#`\\which systemctl`#g" ./linux/limitedadmins.new
sed -i "s#{pkill}#`\\which pkill`#g" ./linux/limitedadmins.new
if [ ! "$sysv" -eq 0 ];then
	echo "Using systemd..."
	yes | cp -rf ./linux/xkeysnail.service ./linux/xkeysnail.service.new
	# yes | cp -rf ./linux/xkeysnail.timer ~/.config/systemd/user/xkeysnail.timer
	sed -i "s#{experimental-caret}#$exp#g" ./linux/xkeysnail.service.new
	if [ "$expsh" != " " ];then
		sed -i "s#{kill-caret}#/usr/bin/pkill -f $expsh#g" ./linux/xkeysnail.service.new
	else
		sed -i "s#{kill-caret}#$expsh#g" ./linux/xkeysnail.service.new
	fi
	sed -i "s/{username}/`whoami`/g" ./linux/xkeysnail.service.new
	sed -i "s#{homedir}#`echo "$HOME"`#g" ./linux/xkeysnail.service.new
	sed -i "s#{xhost}#`\\which xhost`#g" ./linux/xkeysnail.service.new
	sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ./linux/xkeysnail.service.new
else
	echo "Using sysvinit..."
fi
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/kintotray.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/gui/kinto-gui.py
sed -i "s#{homedir}#`echo "$HOME"`#g" ./linux/gui/kinto.desktop.new
sudo mv ./linux/gui/kinto.desktop.new /usr/share/applications/kinto.desktop
sed -i "s#{systemctl}#`\\which systemctl`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{xhost}#`\\which xhost`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/xkeysnail.desktop
# sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/prexk.sh
# sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ~/.config/kinto/prexk.sh

if [[ $dename == "budgie" ]]; then
	perl -pi -e "s/\s{4}(# )(K.*)(# Default SL - Change workspace.*budgie.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "popos" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*popos.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == 'fedora' ]] || [[ $distro == 'fedoralinux' ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*fedora.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
	sed -i "s#{sudo}##g" ./linux/xkeysnail.service.new
	selinuxuser=system_u
	selinuxtype=systemd_unit_file_t
else
	sed -i "s#{sudo}#`\\which sudo` #g" ./linux/xkeysnail.service.new
fi

if [[ $distro == "elementaryos" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*eos.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ "$distro" == "manjaro"* ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*manjaro.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "gnome" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*ubuntu.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "kde" ]]; then
	echo "Applying Cmd-Space to open App Launcher for KDE..."
	perl -pi -e "s/(# )(.*)(#.*kde)/\$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "xfce" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*xfce.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
	perl -pi -e "s/(# )(.*)(# xfce4)/\$2\$3/g" ./linux/kinto.py.new
	perl -pi -e "s/(\w.*)(# Default not-xfce4)/# \$1\$2/g" ./linux/kinto.py.new
fi

if [[ $dename == "xfce" ]] && ls /etc/apt/sources.list.d/enso* 1> /dev/null 2>&1; then
    echo "enso OS detected, applying Cmd-Space for Launchy..."
    perl -pi -e "s/(K\(\"RC-Space)(.*)(# )(xfce4)/\$3\$1\$2\$3\$4/g" ./linux/kinto.py.new >/dev/null 2>&1
    xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary>space" --create --type string --set "launchy"
fi

if ! [[ $1 == "5" || $1 == "uninstall" || $1 == "Uninstall" ]]; then

	mv ./linux/kinto.py.new ~/.config/kinto/kinto.py
	# if [ "$distro" == "fedora" ];then
	if [ ! "$sysv" -eq 0 ];then
		# echo "Using systemd..."
		sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	else
		# echo "Using sysvinit..."
		echo ""
	fi
	if [ -d /usr/lib/systemd/system ];then
		xkeypath="/usr/lib/systemd/system/"
	elif [ -d /lib/systemd/system ];then
		xkeypath="/lib/systemd/system/"
	fi
	xhost +SI:localuser:root
	git clone -b kinto --depth 10 https://github.com/rbreaves/xkeysnail.git
	cd xkeysnail
	giturl=$(git ls-remote --get-url)
	if [ "$giturl" != "https://github.com/rbreaves/xkeysnail.git" ];then
		echo -e "\nreplacing xkeysnail with fork...\n"
		cd ..
		rm -rf ./xkeysnail
		git clone -b kinto --depth 10 https://github.com/rbreaves/xkeysnail.git
		cd xkeysnail
	fi
	sudo pip3 install --upgrade .
	cd ..
	which xkeysnail
	if [ $? -eq 1 ]; then
		echo -e "\nKinto install has \e[1m\033[0;91mfailed\e[0m.\n"
		echo -e "cd into ./xkeysnail"
		echo -e "Run 'sudo pip3 install --upgrade .' to debug issue"
		exit 0
	fi
	sed -i "s#{xkeysnail}#`which xkeysnail`#g" ./linux/limitedadmins.new
	if [[ $distro == 'fedora' ]] || [[ $distro == 'fedoralinux' ]]; then
		echo "Changing SELinux context"
		sudo chcon -v --user=$selinuxuser --type=$selinuxtype "$xkeypath"xkeysnail.service
	fi
	sudo chown root:root ./linux/limitedadmins.new
	# Add a check here for xkeysnail path resolving
	sudo mv ./linux/limitedadmins.new /etc/sudoers.d/limitedadmins
	if [ ! "$sysv" -eq 0 ];then
		# echo "Using systemd..."
		sed -i "s#{xkeysnail}#`which xkeysnail`#g" ./linux/xkeysnail.service.new
		sudo mv ./linux/xkeysnail.service.new "$xkeypath"xkeysnail.service && echo "Service file added to "$xkeypath"xkeysnail.service"

		if [[ $distro == 'fedora' ]] || [[ $distro == 'fedoralinux' ]]; then
			sudo cp "$xkeypath"xkeysnail.service /etc/systemd/system/xkeysnail.service && echo "Copied service file to system..." || echo "Failed to create copy..."
			sudo cp "$xkeypath"xkeysnail.service /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Copied service file to system for graphical target..." || echo "Failed to create copy for graphical target..."
			sudo chown -R root:root /etc/systemd/system/xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
			sudo chown -R root:root /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
			sudo chmod 644 /etc/systemd/system/xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
			sudo chmod 644 /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
		else
			sudo chown -R root:root "$xkeypath"xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
			sudo chmod 644 "$xkeypath"xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
			sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/xkeysnail.service && echo "Created soft symlink..." || echo "Failed to create soft symlink..."
			sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Created soft symlink for graphical target..." || echo "Failed to create soft symlink for graphical target..."
		fi
		sudo systemctl daemon-reload
		sudo systemctl disable xkeysnail
		sudo systemctl stop xkeysnail
	else
		# echo "Using sysvinit..."
		echo ""
		sudo cp ./linux/kinto-service.sh /etc/init.d/kinto
		sudo -E /etc/init.d/kinto stop
		mv /tmp/kinto.log /tmp/kinto.log.bak
	fi
	# sudo systemctl --state=not-found --all | grep xkeysnail
	# if [ "$distro" == "fedora" ];then
	# 	systemctl enable xkeysnail.service
	# else
	# 	sudo systemctl enable xkeysnail.service
	# fi
	# sudo systemctl restart xkeysnail
	sudo pkill -f kintotray &
	# >/dev/null 2>&1
	if [[ $dename == "kde" ]];then
		sed -i "s/systray = true/systray = false/g" ~/.config/kinto/initkb
	fi
	nohup python3 ~/.config/kinto/gui/kinto-gui.py >/dev/null 2>&1 &

	echo -e "Adding xhost fix...\n"

	LINE='xhost +SI:localuser:root'

	if [ ! -e "~/.xprofile" ]; then
		# Ubuntu xhost fix
		echo "$LINE" > ~/.xprofile
		# echo "$LINE" > ~/.xinitrc
	fi
	# Ubuntu xhost fix
	grep -qF -- "$LINE" ~/.xprofile || echo "$LINE" >> ~/.xprofile
	# KDE xhost fix
	# grep -qF -- "$LINE" ~/.bashrc || echo "$LINE" >> ~/.bashrc
	# grep -qF -- "$LINE" ~/.xinitrc || echo "$LINE" >> ~/.xinitrc

	# remove kintox11 login startup
	if test -f "~/.config/autostart/kinto.desktop"; then
		rm ~/.config/autostart/kinto.desktop
	fi

	echo -e "Kinto install is \e[1m\e[32mcomplete\e[0m.\n"

	echo "If the setup wizard fails to appear then please run this command."
	echo -e "~/.config/kinto/gui/kinto-gui.py\n"
	echo -e "You can then either \e]8;;https://google.com\a\e[1m\e[36mG\033[0;91mo\033[0;93mo\e[1m\e[36mg\e[1m\e[32ml\033[0;91me\e[0m\e]8;;\a what dependencies you may be missing\nor \e]8;;https://github.com/rbreaves/kinto/issues/new\?assignees=rbreaves&labels=bug&template=bug_report.md&title=\aopen an issue ticket.\e]8;;\a\n"

	# echo -e "\033[0;91mAfter the installer completes press Any key to re-apply your overlay (Super key) menu launcher.\e[0m\n"

	# if [[ $dename == 'gnome' || $dename == 'budgie' ]];then
	# 	echo "GNOME: gsettings set org.gnome.mutter overlay-key 'super'"
	# elif [[ $dename == 'xfce' ]];then
	# 	echo "XFCE: xfconf-query --channel xfce4-keyboard-shortcuts --property \"/commands/custom/Super_L\" --create --type string --set \"$nlauncher\""
	# fi

	# read -n 1 -s -r -p ""

	# if [[ $dename == 'gnome' || $dename == 'budgie' ]];then
	# 	gsettings set org.gnome.mutter overlay-key 'super'
	# elif [[ $dename == 'xfce' ]];then
	# 	echo -e "\nSetting xfce4 launcher $nlauncher back to Super_L."
	# 	xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/Super_L" --create --type string --set "$nlauncher" && echo "Success."
	# fi
	

	if [ "$distro" == "manjarolinux" ]; then
		echo "If you are using Manjaro and see an error about 'GLIBC_2.xx not found' appears then please update your system."
		echo "sudo pacman -Syu"
	fi

	if [ "$dename" == "gnome" ];then
		echo "Gnome may not support appindicators well, so by default you may need to install packages before enabling the System Tray."
		echo "You may try one of the following extensions."
		echo -e "    1) \e]8;;https://extensions.gnome.org/extension/615/appindicator-support/\aAppIndicator and KStatusNotifierItem Support\e]8;;\a"
		echo -e "    2) \e]8;;https://extensions.gnome.org/extension/1031/topicons/\aTopIcons Plus\e]8;;\a"
		echo -e "\nNote: you may want these supporting packages\n'sudo apt install gnome-tweaks gnome-shell-extension-appindicator gir1.2-appindicator3-0.1'"
	fi

fi
