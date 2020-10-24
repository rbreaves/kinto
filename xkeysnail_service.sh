#!/bin/bash

# set about:config?filter=ui.key.menuAccessKeyFocuses
# to false for wordwise to work in Firefox

typeset -l distro
distro=$(awk -F= '$1=="NAME" { gsub("[\",!,_, ]","",$2);print $2 ;}' /etc/os-release)
typeset -l dename
dename=$(./system-config/dename.sh | cut -d " " -f1)


# Add additional shortcuts if needed, does not modify existing ones

if [[ $dename == 'gnome' || $dename == 'budgie' ]];then
	if [[ $(gsettings get org.gnome.mutter overlay-key | grep "''\|' '" | wc -l) != 1 ]];then
		bound=$(gsettings get org.gnome.mutter overlay-key)
		echo "Overlay key, " $bound ", detected. Will be removing so Super-Space can remap to Cmd-Space for app launching.."
		echo "Overlay key, Super, detected. Will be removing so Super-Space can remap to Cmd-Space for app launching.."
		gsettings set org.gnome.mutter overlay-key ''
	fi
fi

# if ls /etc/apt/sources.list.d/system76* 1> /dev/null 2>&1; then
if [[ $distro == 'popos' ]]; then
	pip3 install pillow
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

if [[ $dename == "kde" ]]; then
	if [[ $distroy == "manjarolinux" ]]; then
		sudo ./system-config/unipkg.sh vte3
	else
		sudo ./system-config/unipkg.sh libvte-2.91-dev
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
	if [[ $(perl -ne 'print if /^SELINUX=enforcing/' /etc/selinux/config | wc -l) != 0 ]]; then
		while true; do
		read -rep $'\nWould you like to update your SELinux state from enforcing to permissive? (y/n)\n' yn
		case $yn in
			[Yy]* ) setSE='yes'; break;;
			[Nn]* ) exp='no'; expsh=" " break;;
			# * ) echo "Please answer yes or no.";;
		esac
		done	

		if [[ $yn == "yes" ]]; then
			sed -i "s/SELINUX=enforcing/SELINUX=permissive/g" /etc/selinux/config
			echo "/etc/selinux/config has been updated. Please reboot your computer before continuing."
			exit 0
		fi
	else
		echo "SELinux state should be ok for Kinto to install"
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


function uninstall {

	while true; do
	read -rep $'\nPress R to restore your original shortcuts.\nPress F to reset to factory shortcuts. (f/r)\n' yn
		case $yn in
			[Ff]* ) yn="f"; break;;
			[Rr]* ) yn="r";break;;
			* ) echo "Please answer yes or no.";;
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
			echo "gsettings set org.gnome.mutter overlay-key 'super'"
			gsettings set org.gnome.mutter overlay-key 'super'
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
				if ! [ -f ./system-config/budgie-daemon_10.5.1 ]; then
					wget https://github.com/rbreaves/budgie-desktop/blob/binaries/binaries/budgie-daemon_10.5.1?raw=true -O ./system-config/budgie-daemon_10.5.1
				fi
				bdmd5=$(md5sum /usr/bin/budgie-daemon | awk '{ print $1 }')
				newbdmd5=$(md5sum ./system-config/budgie-daemon_10.5.1 | awk '{ print $1 }')
				if [ "$bdmd5" != "$newbdmd5" ]; then
					cp /usr/bin/budgie-daemon ./budgie-daemon_"$budgieVersion".bak
					sudo pkill budgie-daemon && sudo cp ./system-config/budgie-daemon_10.5.1 /usr/bin/budgie-daemon
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
					if ! [ -f ./system-config/budgie-daemon_10.5.1 ]; then
						wget https://github.com/rbreaves/budgie-desktop/raw/43d3b44243b0bcaee3262a79818024a651475b58/binaries/budgie-daemon_10.5.1 -O ./system-config/budgie-daemon_10.5.1
					fi
					cp /usr/bin/budgie-daemon ./budgie-daemon_"$budgieVersion".bak
					sudo pkill budgie-daemon && sudo cp ./system-config/budgie-daemon_10.5.1 /usr/bin/budgie-daemon
					echo "Updated Budgie to use App Switching Patch"
				fi
			fi
		fi
	fi
}

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
# 	sudo ./system-config/unipkg.sh inotify-tools
# fi
if ! [ -x "$(command -v pip3)" ]; then
	echo "Will need to install python3-pip..."
	sudo ./system-config/unipkg.sh python3-pip
fi
if ! [ -x "$(command -v python3-config)" ]; then
	if [ "$distro" == "ubuntu" ] || [ "$distro" == "debian" ] || [ "$distro" == 'linuxmint' ]; then
		pydev="python3-dev"
	elif [ "$distro" == "fedora" ]; then
		pydev="python3-devel"
	fi
	if [ "$distro" == "gnome" ] || [ "$distro" == "fedora" ] || [ "$distro" == "debian" ] || [ "$distro" == 'linuxmint' ]; then
		echo "Will need to install $pydev..."
		sudo ./system-config/unipkg.sh "$pydev"
	fi
fi
if ! [ -x "$(command -v xhost)" ] || ! [ -x "$(command -v gcc)" ]; then
	if [ "$distro" == "\"manjaro linux\"" ]; then
		sudo ./system-config/unipkg.sh "xorg-xhost gcc"
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
yes | cp -rf ./xkeysnail-config/xkeysnail.desktop ~/.config/kinto/xkeysnail.desktop

# yes | cp -rf ./xkeysnail-config/xkeystart.sh ~/.config/kinto/xkeystart.sh

# *** More testing needing, universal way of killing kinto on user log out? ***
# yes | sudo cp -rf xkeysnail-config/root_logoff.sh /usr/local/bin/logoff.sh
# sudo chown root:root /usr/local/bin/logoff.sh
# sudo chmod u+rwx /usr/local/bin/logoff.sh
# sudo chmod go-w+rx /usr/local/bin/logoff.sh
# *** End universal killing of kinto

# logoff fix - not solid for every os. Prevents missed 1 character input on login
# yes | sudo cp -rf xkeysnail-config/gnome_logoff.sh ~/.config/kinto/logoff.sh

echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)" > ~/.config/kinto/version
yes | cp -rf ./xkeysnail-config/kinto.py ./xkeysnail-config/kinto.py.new
yes | cp -rf ./xkeysnail-config/limitedadmins ./xkeysnail-config/limitedadmins.new
yes | cp -rf ./xkeysnail-config/gui/ ~/.config/kinto/
yes | cp -nrf ./xkeysnail-config/initkb ~/.config/kinto/initkb
yes | cp -rf ./xkeysnail-config/killdups.sh ~/.config/kinto/killdups.sh
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/kintotray.py ~/.config/kinto/kintotray.py
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/kintotray.desktop ~/.config/kinto/kintotray.desktop
yes | cp -rf ./xkeysnail-config/gui/kinto.desktop ./xkeysnail-config/gui/kinto.desktop.new
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color.svg
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color-48.svg
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/icons/kinto-invert-16.svg ~/.config/kinto/kinto-invert.svg
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/icons/kinto-solid-16.svg ~/.config/kinto/kinto-solid.svg
yes | cp -rf ./xkeysnail-config/trayapps/appindicator/icons/kinto.svg ~/.config/kinto/kinto.svg
# yes | cp -rf ./system-config/caret_status_xkey.sh ~/.config/kinto/caret_status_xkey.sh
yes | cp -rf ./xkeysnail-config/xkeysnail.service ./xkeysnail-config/xkeysnail.service.new
# yes | cp -rf ./xkeysnail-config/xkeysnail.timer ~/.config/systemd/user/xkeysnail.timer
sed -i "s#{experimental-caret}#$exp#g" ./xkeysnail-config/xkeysnail.service.new
if [ "$expsh" != " " ];then
	sed -i "s#{kill-caret}#/usr/bin/pkill -f $expsh#g" ./xkeysnail-config/xkeysnail.service.new
else
	sed -i "s#{kill-caret}#$expsh#g" ./xkeysnail-config/xkeysnail.service.new
fi
sed -i "s/{username}/`whoami`/g" ./xkeysnail-config/xkeysnail.service.new
sed -i "s#{homedir}#`echo "$HOME"`#g" ./xkeysnail-config/xkeysnail.service.new
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/kintotray.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/gui/kinto-gui.py
sed -i "s#{homedir}#`echo "$HOME"`#g" ./xkeysnail-config/gui/kinto.desktop.new
sudo mv ./xkeysnail-config/gui/kinto.desktop.new /usr/share/applications/kinto.desktop
sed -i "s#{xhost}#`\\which xhost`#g" ./xkeysnail-config/xkeysnail.service.new
sed -i "s/{username}/`whoami`/g" ./xkeysnail-config/limitedadmins.new
sed -i "s#{systemctl}#`\\which systemctl`#g" ./xkeysnail-config/limitedadmins.new
sed -i "s#{pkill}#`\\which pkill`#g" ./xkeysnail-config/limitedadmins.new
sed -i "s#{xkeysnail}#/usr/local/bin/xkeysnail#g" ./xkeysnail-config/limitedadmins.new
sudo chown root:root ./xkeysnail-config/limitedadmins.new
sudo mv ./xkeysnail-config/limitedadmins.new /etc/sudoers.d/limitedadmins
sed -i "s#{systemctl}#`\\which systemctl`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{xhost}#`\\which xhost`#g" ~/.config/kinto/xkeysnail.desktop
sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/xkeysnail.desktop
# sed -i "s#{homedir}#`echo "$HOME"`#g" ~/.config/kinto/prexk.sh
sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ./xkeysnail-config/xkeysnail.service.new
# sed -i "s/{displayid}/`echo "$DISPLAY"`/g" ~/.config/kinto/prexk.sh

if [[ $dename == "budgie" ]]; then
	perl -pi -e "s/\s{4}(# )(K.*)(# Default SL - Change workspace.*budgie.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "popos" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*popos.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "fedora" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*fedora.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $distro == "elementaryos" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*eos.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ "$distro" == "manjaro"* ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*manjaro.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "gnome" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*ubuntu.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "kde" ]]; then
	echo "Applying Cmd-Space to open App Launcher for KDE..."
	perl -pi -e "s/(# )(.*)(#.*kde)/\$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
fi

if [[ $dename == "xfce" ]]; then
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*xfce.*)/    \$2\$3/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
	perl -pi -e "s/(# )(.*)(# xfce4)/\$2\$3/g" ./xkeysnail-config/kinto.py.new
	perl -pi -e "s/(\w.*)(# Default not-xfce4)/# \$1\$2/g" ./xkeysnail-config/kinto.py.new
fi

if [[ $dename == "xfce" ]] && ls /etc/apt/sources.list.d/enso* 1> /dev/null 2>&1; then
    echo "enso OS detected, applying Cmd-Space for Launchy..."
    perl -pi -e "s/(K\(\"RC-Space)(.*)(# )(xfce4)/\$3\$1\$2\$3\$4/g" ./xkeysnail-config/kinto.py.new >/dev/null 2>&1
    xfconf-query --channel xfce4-keyboard-shortcuts --property "/commands/custom/<Primary>space" --create --type string --set "launchy"
fi

if ! [[ $1 == "5" || $1 == "uninstall" || $1 == "Uninstall" ]]; then
	mv ./xkeysnail-config/kinto.py.new ~/.config/kinto/kinto.py
	# if [ "$distro" == "fedora" ];then
	sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	if [ -d /usr/lib/systemd/system ];then
		xkeypath="/usr/lib/systemd/system/"
	elif [ -d /lib/systemd/system ];then
		xkeypath="/lib/systemd/system/"
	fi
	sudo mv ./xkeysnail-config/xkeysnail.service.new "$xkeypath"xkeysnail.service && echo "Service file added to "$xkeypath"xkeysnail.service"
	sudo chown -R root:root "$xkeypath"xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
	sudo chmod 644 "$xkeypath"xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/xkeysnail.service && echo "Created soft symlink..." || echo "Failed to create soft symlink..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Created soft symlink for graphical target..." || echo "Failed to create soft symlink for graphical target..."
	xhost +SI:localuser:root
	git clone --depth 10 https://github.com/rbreaves/xkeysnail.git
	cd xkeysnail
	git pull --depth 10
	git checkout 51c369084e0045a8410d227bab52411bf84fb65b
	giturl=$(git ls-remote --get-url)
	if [ "$giturl" != "https://github.com/rbreaves/xkeysnail.git" ];then
		echo -e "\nreplacing xkeysnail with fork...\n"
		cd ..
		rm -rf ./xkeysnail
		git clone --depth 10 https://github.com/rbreaves/xkeysnail.git
		cd xkeysnail
		git checkout 51c369084e0045a8410d227bab52411bf84fb65b
	fi
	sudo pip3 install --upgrade .
	cd ..
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
	if ! [[ $dename == "gnome" || $dename == "kde" ]];then
		sudo pkill -f kintotray >/dev/null 2>&1
	else
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

elif [[ $1 == "5" || $1 == "uninstall" || $1 == "Uninstall" ]]; then
	echo "Uninstalling Kinto - xkeysnail (udev)"
	uninstall
	removeAppleKB
	pkill -f kintotray >/dev/null 2>&1
	sudo systemctl stop xkeysnail >/dev/null 2>&1
	sudo systemctl disable xkeysnail >/dev/null 2>&1
	sudo pkill -f bin/xkeysnail >/dev/null 2>&1
	sudo pkill -f "is-active xkeysnail" >/dev/null 2>&1
	sudo rm /etc/sudoers.d/limitedadmins >/dev/null 2>&1
	rm ~/.config/autostart/xkeysnail.desktop >/dev/null 2>&1
	rm ~/.config/autostart/kintotray.desktop  >/dev/null 2>&1
	rm -rf ~/.config/kinto >/dev/null 2>&1
	sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	sudo rm /usr/share/applications/kinto.desktop  >/dev/null 2>&1
	sudo rm /etc/systemd/system/graphical.target.wants/xkeysnail.service >/dev/null 2>&1
	sudo rm /usr/lib/systemd/system/xkeysnail.service >/dev/null 2>&1
	sudo rm /lib/systemd/system/xkeysnail.service >/dev/null 2>&1
	if [ -f /usr/local/bin/logoff.sh ];then
		sudo rm /usr/local/bin/logoff.sh
	fi
	sudo systemctl daemon-reload
	# sudo systemctl --state=not-found --all | grep xkeysnail
	exit 0
else
	echo "Expected argument was not provided"
fi
