#!/bin/bash

# set about:config?filter=ui.key.menuAccessKeyFocuses
# to false for wordwise to work in Firefox

typeset -l sessiontype
sessiontype=$XDG_SESSION_TYPE

if [ "$sessiontype" == "wayland" ]; then 
	echo 
	echo "  ==================================================== "
	echo "  Seems like you may be running Wayland, not Xorg/X11. "
	echo "     Kinto/xkeysnail doesn't work yet under Wayland.   "
	echo "  ==================================================== "
	echo  
elif ! [ "$sessiontype" == "x11" ]; then 
	echo 
	echo "  ==================================================== "
	echo "      Make sure you're in an Xorg/X11 environment.     "
	echo "     Kinto/xkeysnail doesn't work yet under Wayland.  "
	echo "  ==================================================== "
	echo 
elif [ "$sessiontype" == "x11" ]; then 
	echo 
	echo "  X11 detected... good to go."
	echo 
fi

if ! [ "$sessiontype" == "x11" ]; then
	while true; do
		read -rep $'  Are you sure you want to continue the install? (y/n): ' continue
		case $continue in
			[yY]* ) break;;
			[nN]* ) echo -e "\n  Install canceled.\n\n  Log in with Xorg/X11 option and try again.\n"; exit 0; break;;
			* ) ;;
		esac
	done
fi

typeset -l distro
distro=$(awk -F= '$1=="NAME" { gsub("[\",!,_, ]","",$2);print $2 ;}' /etc/os-release)
typeset -l dename
dename=$(./linux/system-config/dename.sh | cut -d " " -f1)

typeset -l desktopsession
desktopsession=$(echo $DESKTOP_SESSION)
typeset -l currentdesktop
currentdesktop=$(env | grep -i XDG_CURRENT_DESKTOP | awk -F"=" '/=/{print $2}')

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
			cp /etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
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

if ! [ -x "$(command -v pip3)" ]; then
	if [ "$distro" == "ubuntu" ]; then
		echo 
		echo "Ubuntu-based..."
		echo 
		echo "Will need to install pip..."
		sudo ./linux/system-config/unipkg.sh "curl python3-setuptools"
		echo 
		echo "Downloading pip installer... "
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		sudo python3 get-pip.py --upgrade && rm get-pip.py
	elif [ "$distro" == "manjarolinux" ]; then
		if [ "$currentdesktop" == "lxqt" ]; then
			echo 
			echo "Found Manjaro LXQt..." 
			echo 
			echo "Will need to install python-pip..."
			sudo ./linux/system-config/unipkg.sh "python-evdev python-wheel"
			sudo ./linux/system-config/unipkg.sh "python-setuptools python-pip"
		elif [ "$dename" == "kde" ]; then
			echo 
			echo "Found Manjaro KDE..."
			echo 
			echo "Will need to install python-pip..."
			sudo ./linux/system-config/unipkg.sh "python-setuptools python-pip"
		else 
			echo 
			echo "Found Manjaro"
			echo 
			echo "Will need to install pip wheel evdev setuptools"
			sudo ./linux/system-config/unipkg.sh "python-evdev python-wheel"
			sudo ./linux/system-config/unipkg.sh "python-setuptools python-pip"
		fi
	else
		echo 
		echo "Will need to install python3-pip..."
		sudo ./linux/system-config/unipkg.sh "python3-setuptools python3-pip"
	fi
fi

pip3 install pillow

# Add additional shortcuts if needed, does not modify existing ones

if [[ $dename == 'gnome' || $dename == 'budgie' ]];then
	if [[ $(gsettings get org.gnome.mutter overlay-key | grep "''\|' '" | wc -l) != 1 ]];then
		bound=$(gsettings get org.gnome.mutter overlay-key)
		echo "Overlay key, " $bound ", detected. Will be removing so Super-Space can remap to Cmd-Space for app launching.."
		gsettings set org.gnome.mutter overlay-key ''
	fi
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
fi

if ! [ -x "$(command -v xhost)" ] || ! [ -x "$(command -v gcc)" ]; then
	if [ "$distro" == "manjarolinux" ]; then
		sudo ./linux/system-config/unipkg.sh "xorg-xhost gcc"
	fi
fi

if [[ $dename == "kde" ]]; then
	if [[ $distro == "manjarolinux" ]]; then
		sudo ./linux/system-config/unipkg.sh vte3
	elif [[ $distro == "fedora" ]]; then
		sudo ./linux/system-config/unipkg.sh vte291
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

if [[ $distro == 'fedora' ]]; then

	echo "Checking SELinux status..."
	echo 
	
	if [[ $(perl -ne 'print if /^SELINUX=enforcing/' /etc/selinux/config | wc -l) != 0 ]]; then
	
		while true; do
			read -rep $'\nWould you like to update your SELinux state from enforcing to permissive? (y/n): ' yn
			case $yn in
				[Yy]* ) setSE='yes'; break;;
				[Nn]* ) exp='no'; expsh=" " break;;
				* ) echo -e "\nPlease answer [y]es or [n]o.";;
			esac
		done	

		if [[ $setSE == "yes" ]]; then
			sudo sed -i "s/SELINUX=enforcing/SELINUX=permissive/g" /etc/selinux/config
			
			if [[ $(perl -ne 'print if /^SELINUX=permissive/' /etc/selinux/config | wc -l) != 0 ]] && \
			   [[ $(perl -ne 'print if /^SELINUX=enforcing/' /etc/selinux/config | wc -l) != 1 ]]; then
			   	echo 
				echo "================================================================================"
				echo "   SUCCESS: /etc/selinux/config has been updated. Please reboot your computer    "
				echo "            before continuing with Kinto setup.                                 "
				echo "================================================================================"
				echo 
				exit 0
			else 
				echo 
				echo "================================================================================"
				echo "ERROR: Could not update /etc/selinux/config. Please update the config file to read "
				echo "       SELINUX=permissive and reboot your computer before continuing with setup."
				echo "================================================================================"
				echo 
				exit 0
			fi
		fi
		
	# Check to see if SELinux is actually in Permissive mode. Exit and prompt user to reboot if not.  
	elif [[ $(perl -ne 'print if /^SELINUX=permissive/' /etc/selinux/config | wc -l) != 0 ]] && \
	     [[ $(getenforce | grep -c -i enforcing) != 0 ]]; then
	  	echo 
		echo "================================================================================"
		echo "  ERROR: You MUST reboot to enable SELinux permissive mode before continuing.   "
		echo "================================================================================"
		echo 
		exit 0
	else
		echo "SELinux state should be ok for Kinto to install"
		echo 
	fi
	
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

if [ "$desktopsession" == "lubuntu" ]; then
	echo 
	echo "Will need to install gir1.2-vte-2.91... "
	sudo ./linux/system-config/unipkg.sh gir1.2-vte-2.91
fi

if [ "$distro" == "opensusetumbleweed" ]; then
	echo 
	echo "Will need to install typelib-1_0-Vte-2.91... "
	sudo ./linux/system-config/unipkg.sh typelib-1_0-Vte-2.91
	echo 
	echo "Will need to install python3-wheel... "
	sudo ./linux/system-config/unipkg.sh python3-wheel
	echo 
	echo "Adding user to systemd-journal group..."
	sudo usermod -a -G systemd-journal $(whoami)
	echo 
	echo "User is now in systemd-journal group, but you will "
	echo "need to log out and back in to view the journal..."
	echo 
	sleep 3
fi

if ! [ -x "$(command -v gcc)" ]; then
	echo 
	echo "Will need to install gcc... "
	sudo ./linux/system-config/unipkg.sh gcc
fi

if ! [ -x "$(command -v git)" ]; then
	echo 
	echo "Will need to install git... "
	sudo ./linux/system-config/unipkg.sh git
fi

if ! [ -x "$(command -v python3-config)" ]; then
	if [ "$distro" == "ubuntu" ] || [ "$distro" == "debian" ] || [ "$distro" == 'linuxmint' ]; then
		pydev="python3-dev"
	elif [ "$distro" == "fedora" ] || [ "$distro" == "opensusetumbleweed" ]; then
		pydev="python3-devel"
	fi
	if [ "$distro" == "ubuntu" ] || \
	   [ "$distro" == "gnome" ] || \
	   [ "$distro" == "fedora" ] || \
	   [ "$distro" == "debian" ] || \
	   [ "$distro" == 'linuxmint' ] || \
	   [ "$distro" == "opensusetumbleweed" ]; then
		echo 
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

if [ "$distro" == 'linuxmint' ]; then
	pip3 install setuptools
fi

# echo "Transferring files..."
mkdir -p ~/.config/kinto

# KDE xhost fix
# mkdir -p ~/.kde/Autostart
# echo -e '#!/bin/sh\rxhost +SI:localuser:root' > ~/.kde/Autostart/kintohost.sh
# chmod +x ~/.kde/Autostart/kintohost.sh

# KDE startup - xhost fix
mkdir -p ~/.config/autostart
yes | cp -rf ./linux/xkeysnail.desktop ~/.config/kinto/xkeysnail.desktop

# yes | cp -rf ./linux/xkeystart.sh ~/.config/kinto/xkeystart.sh

# *** More testing needing, universal way of killing kinto on user log out? ***
# yes | sudo cp -rf linux/root_logoff.sh /usr/local/bin/logoff.sh
# sudo chown root:root /usr/local/bin/logoff.sh
# sudo chmod u+rwx /usr/local/bin/logoff.sh
# sudo chmod go-w+rx /usr/local/bin/logoff.sh
# *** End universal killing of kinto

# logoff fix - not solid for every os. Prevents missed 1 character input on login
# yes | sudo cp -rf linux/gnome_logoff.sh ~/.config/kinto/logoff.sh

echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)" > ~/.config/kinto/version
yes | cp -rf ./linux/kinto.py ./linux/kinto.py.new
yes | cp -rf ./linux/limitedadmins ./linux/limitedadmins.new
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
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/kintotray.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/gui/kinto-gui.py
sed -i "s#{homedir}#`echo "$HOME"`#g" ./linux/gui/kinto.desktop.new
sudo mv ./linux/gui/kinto.desktop.new /usr/share/applications/kinto.desktop
sed -i "s#{xhost}#`\\which xhost`#g" ./linux/xkeysnail.service.new
sed -i "s/{username}/`whoami`/g" ./linux/limitedadmins.new
sed -i "s#{systemctl}#`\\which systemctl`#g" ./linux/limitedadmins.new
sed -i "s#{pkill}#`\\which pkill`#g" ./linux/limitedadmins.new
sed -i "s#{systemctl}#`\\which systemctl`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{xhost}#`\\which xhost`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/xkeysnail.desktop
# sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/prexk.sh
sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ./linux/xkeysnail.service.new
# sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ~/.config/kinto/prexk.sh

if [[ $dename == "budgie" ]]; then
	perl -pi -e "s/\s{4}(# )(K.*)(# Default SL - Change workspace.*budgie.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "popos" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*popos.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "fedora" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*fedora.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
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

# Use xfce4 tweaks also on Linux Mint Cinnamon
if [[ $dename == "cinnamon" ]] && [[ $distro == "linuxmint" ]]; then
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
	sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	if [ -d /usr/lib/systemd/system ];then
		xkeypath="/usr/lib/systemd/system/"
	elif [ -d /lib/systemd/system ];then
		xkeypath="/lib/systemd/system/"
	fi
	xhost +SI:localuser:root
	git clone --depth 10 https://github.com/rbreaves/xkeysnail.git
	cd xkeysnail
	git checkout kinto
	giturl=$(git ls-remote --get-url)
	if [ "$giturl" != "https://github.com/rbreaves/xkeysnail.git" ];then
		echo -e "\nreplacing xkeysnail with fork...\n"
		cd ..
		rm -rf ./xkeysnail
		git clone --depth 10 https://github.com/rbreaves/xkeysnail.git
		cd xkeysnail
		git checkout kinto
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
	
	sed -i "s#{xkeysnail}#`which xkeysnail`#g" ./linux/xkeysnail.service.new
	sed -i "s#{xkeysnail}#`which xkeysnail`#g" ./linux/limitedadmins.new
	
	if [ "$distro" == "opensusetumbleweed" ]; then
		sed -i "s#'/usr/bin/xhost#'export DISPLAY=`echo $DISPLAY` \&\& /usr/bin/xhost#g" ./linux/xkeysnail.service.new
	fi
	
	sudo mv ./linux/xkeysnail.service.new "$xkeypath"xkeysnail.service && echo "Service file added to "$xkeypath"xkeysnail.service"
	sudo chown root:root ./linux/limitedadmins.new
	# Add a check here for xkeysnail path resolving
	sudo mv ./linux/limitedadmins.new /etc/sudoers.d/limitedadmins
	sudo chown -R root:root "$xkeypath"xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
	sudo chmod 644 "$xkeypath"xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/xkeysnail.service && echo "Created soft symlink..." || echo "Failed to create soft symlink..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Created soft symlink for graphical target..." || echo "Failed to create soft symlink for graphical target..."
	sudo systemctl daemon-reload
	sudo systemctl disable xkeysnail
	sudo systemctl stop xkeysnail
	# sudo systemctl --state=not-found --all | grep xkeysnail
	# if [ "$distro" == "fedora" ];then
	# 	systemctl enable xkeysnail.service
	# else
	# 	sudo systemctl enable xkeysnail.service
	# fi
	# sudo systemctl restart xkeysnail
	sudo pkill -f kintotray >/dev/null 2>&1
	if [[ $dename == "gnome" || $dename == "kde" ]];then
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

	if [ "$distro" == "linuxmint" ] && [ "$dename" == "cinnamon" ]; then
		echo
		echo "======================================================================================"
		echo "======== ATTENTION! SPECIAL INSTRUCTIONS FOR CINNAMON DESKTOP ON LINUX MINT: ========="
		echo "======================================================================================"
		echo 
		echo "To get Alt+Tab (cycle windows) and Ctrl+H (minimize/hide window) working correctly in "
		echo "Mint Cinnamon after activating Kinto via the GUI installer window: "
		echo 
		echo "Open the Keyboard settings app from the Cinnamon main menu. Go to the Shortcuts tab. "
		echo 
		echo "Under General -> \"Cycle through open windows\": "
		echo "  Click \"unassigned\" under the existing \"Alt+Tab\" shortcut until it says \"Pick an accelerator\"."
		echo "  Press physical Alt+Tab (or Cmd+Tab) keys to add a second shortcut (will show as \"Ctrl+Backslash\". "
		echo 
		echo "Optional: Set \"Cycle backwards through open windows\":"
		echo "  Press physical Shift+Alt+Tab (will show as \"Shift+Ctrl+|\"). [Vertical bar/pipe character] "
		echo 
		echo "Under Windows -> \"Minimize window\": "
		echo "  Press physical Ctrl+H keys to assign the shortcut to show as \"Super+H\". "
		echo "  Now physical Alt+H (or Cmd+H on Apple keyboard) will minimize (hide) windows. "
		echo 
		echo "Kinto may have crashed if you Alt+Tabbed in the GUI window before fixing the shortcuts. "
		echo "Just use the tray icon menu or quit and re-open the Kinto GUI and restart Kinto from menu. "
		echo 
		echo "======================================================================================"
		echo "===== END OF SPECIAL INSTRUCTIONS FOR CINNAMON DESKTOP ON LINUX MINT (See above) ====="
		echo "======================================================================================"
		echo 
	fi
	
	if [ "$distro" == "manjarolinux" ]; then
		echo 
		echo "If you are using Manjaro and see an error about 'GLIBC_2.xx not found' appears then please update your system."
		echo "sudo pacman -Syu"
		echo 
	fi

	if [ "$dename" == "gnome" ];then
		echo 
		echo "Gnome may not support appindicators well, so by default you may need to install packages before enabling the System Tray."
		echo "You may try one of the following extensions."
		echo -e "    1) \e]8;;https://extensions.gnome.org/extension/615/appindicator-support/\aAppIndicator and KStatusNotifierItem Support\e]8;;\a"
		echo -e "    2) \e]8;;https://extensions.gnome.org/extension/1031/topicons/\aTopIcons Plus\e]8;;\a"
		echo -e "\nNote: you may want these supporting packages\n'sudo apt install gnome-tweaks gnome-shell-extension-appindicator gir1.2-appindicator3-0.1'"
	fi
	
	if [ "$distro" == "opensusetumbleweed" ]; then 
		sudo systemctl enable xkeysnail.service
	fi

fi
