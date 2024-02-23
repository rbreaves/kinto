#!/bin/bash
#
# The Fedora 33 specific installer for xkeysnail
#
# I would rather implement this using either a more elegant language like ruby or python
# but I did not want to go too far for now either, so i sticked with reorganizing the
# existing code and keeping only the parts applicable for fedora, since that is what I
# use most of the time and thus have the best knowledge about.

# Find out the desktop environment name using the existing means
declare -l dename
dename=$(./linux/system-config/dename.sh | cut -d " " -f1)

echo "Desktop environment is $dename"

# Fail when it is now gnome for now. All supported desktop environments should be
# explicitly added here when the specific functions for them are also implemented
[[ $dename == "gnome" || $dename == "kde" ]] || echo "Only gnome and KDE supported at the moment. Exiting." && exit 1

# External interface
#
# These two functions must be provided by every distro and version specific implementation

function install {
	echo "Running intallation for Fedora 33"
	prepare_for_$dename
	install_common_components
	prepare_dirs_and_files
	do_something_i_do_not_understand_to_the_kinto_py_file
	perform_actual_installation
	finish_for_$dename
}

function uninstall {
	echo "Running unintallation for Fedora 33"
	# TODO: implement the tear down
}

# "Private" functions

function install_common_components {
	if ! [ -x "$(command -v pip3)" ]; then
		echo "Will need to install python3-pip..."
		sudo dnf check-update
		sudo dnf install -y python3-pip
	fi

	if ! [ -x "$(command -v python3-config)" ]; then
		echo "Will need to install python3-devel..."
		sudo dnf install python3-devel
	fi
}

function prepare_dirs_and_files {
	mkdir -p ~/.config/kinto
	echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)" >~/.config/kinto/version
	yes | cp -rf ./linux/kinto.py ./linux/kinto.py.new
	yes | cp -rf ./linux/gui/ ~/.config/kinto/
	yes | cp -nrf ./linux/initkb ~/.config/kinto/initkb
	yes | cp -rf ./linux/killdups.sh ~/.config/kinto/killdups.sh # TODO: There must be a better way for what this does btw.
	yes | cp -rf ./linux/trayapps/appindicator/kintotray.py ~/.config/kinto/kintotray.py
	yes | cp -rf ./linux/trayapps/appindicator/kintotray.desktop ~/.config/kinto/kintotray.desktop
	yes | cp -rf ./linux/gui/kinto.desktop ./linux/gui/kinto.desktop.new
	yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color.svg
	yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-color-16.svg ~/.config/kinto/kinto-color-48.svg
	yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-invert-16.svg ~/.config/kinto/kinto-invert.svg
	yes | cp -rf ./linux/trayapps/appindicator/icons/kinto-solid-16.svg ~/.config/kinto/kinto-solid.svg
	yes | cp -rf ./linux/trayapps/appindicator/icons/kinto.svg ~/.config/kinto/kinto.svg
	yes | cp -rf ./linux/xkeysnail.service ./linux/xkeysnail.service.new
	sed -i "s/{username}/$(whoami)/g" ./linux/xkeysnail.service.new
	sed -i "s#{homedir}#$(echo "$HOME")#g" ./linux/xkeysnail.service.new
	sed -i "s#{homedir}#$(echo "$HOME")#g" ~/.config/kinto/kintotray.desktop
	sed -i "s#{homedir}#$(echo "$HOME")#g" ~/.config/kinto/gui/kinto-gui.py
	sed -i "s#{homedir}#$(echo "$HOME")#g" ./linux/gui/kinto.desktop.new
	sudo mv ./linux/gui/kinto.desktop.new /usr/share/applications/kinto.desktop
	sed -i "s#{xhost}##g" ./linux/xkeysnail.service.new
	sed -i "s#{systemctl}#$(\which systemctl)#g" ~/.config/kinto/xkeysnail.desktop
	sed -i "s#{xhost}#$(\which xhost)#g" ~/.config/kinto/xkeysnail.desktop
	sed -i "s#{homedir}#$(echo "$HOME")#g" ~/.config/kinto/xkeysnail.desktop
	sed -i "s/{displayid}/$(echo "$DISPLAY")/g" ./linux/xkeysnail.service.new
	sed -i "s#{sudo}##g" ./linux/xkeysnail.service.new
}

# TODO: Find out what this is. Some search and replace i guess, but what and why?
function do_something_i_do_not_understand_to_the_kinto_py_file {
	perl -pi -e "\s{4}(# )(K.*)(# SL - .*fedora.*)/    \$2\$3/g" ./linux/kinto.py.new >/dev/null 2>&1
}

# The actual installation process.
# This should be sliced into generic parts we can reuse for other distros and versions
# and the distro specific things
function perform_actual_installation {
	mv ./linux/kinto.py.new ~/.config/kinto/kinto.py
	sudo rm /etc/systemd/system/xkeysnail.service >/dev/null 2>&1
	xkeypath="/usr/lib/systemd/system/"
	xhost +SI:localuser:root
	git clone --depth 10 https://github.com/rbreaves/xkeysnail.git
	cd xkeysnail
	git checkout kinto
	giturl=$(git ls-remote --get-url)

	if [ "$giturl" != "https://github.com/rbreaves/xkeysnail.git" ]; then
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

	sed -i "s#{xkeysnail}#$(which xkeysnail)#g" ./linux/xkeysnail.service.new
	sed -i "s#{xkeysnail}#$(which xkeysnail)#g" ./linux/limitedadmins.new
	sudo mv ./linux/xkeysnail.service.new "$xkeypath"xkeysnail.service && echo "Service file added to "$xkeypath"xkeysnail.service"
	echo "Changing SELinux context"
	sudo chcon -v --user=$selinuxuser --type=$selinuxtype "$xkeypath"xkeysnail.service
	sudo chown root:root ./linux/limitedadmins.new
	sudo chown -R root:root "$xkeypath"xkeysnail.service && echo "Ownership set for root..." || echo "Failed to set ownership..."
	sudo chmod 644 "$xkeypath"xkeysnail.service && echo "Permissions set to 644..." || echo "Failed to set permissions..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/xkeysnail.service && echo "Created soft symlink..." || echo "Failed to create soft symlink..."
	sudo ln -s "$xkeypath"xkeysnail.service /etc/systemd/system/graphical.target.wants/xkeysnail.service && echo "Created soft symlink for graphical target..." || echo "Failed to create soft symlink for graphical target..."
	sudo systemctl daemon-reload
	sudo systemctl disable xkeysnail
	sudo systemctl stop xkeysnail
	sudo pkill -f kintotray >/dev/null 2>&1

	nohup python3 ~/.config/kinto/gui/kinto-gui.py >/dev/null 2>&1 &

	echo -e "Adding xhost fix...\n"

	LINE='xhost +SI:localuser:root'

	echo -e "Kinto install is \e[1m\e[32mcomplete\e[0m.\n"

	echo "If the setup wizard fails to appear then please run this command."
	echo -e "~/.config/kinto/gui/kinto-gui.py\n"
	echo -e "You can then either \e]8;;https://google.com\a\e[1m\e[36mG\033[0;91mo\033[0;93mo\e[1m\e[36mg\e[1m\e[32ml\033[0;91me\e[0m\e]8;;\a what dependencies you may be missing\nor \e]8;;https://github.com/rbreaves/kinto/issues/new\?assignees=rbreaves&labels=bug&template=bug_report.md&title=\aopen an issue ticket.\e]8;;\a\n"
}

# Gnome specific steps

function prepare_for_gnome {
	echo "Running gnome specific steps"
	reset_mutter_overlay_key
	set_show_desktop_shortcut_if_applicable
	sed -i "s/systray = true/systray = false/g" ~/.config/kinto/initkb
}

function finish_for_gnome {
	echo "Gnome may not support appindicators well, so by default you may need to install packages before enabling the System Tray."
	echo "You may try one of the following extensions."
	echo -e "    1) \e]8;;https://extensions.gnome.org/extension/615/appindicator-support/\aAppIndicator and KStatusNotifierItem Support\e]8;;\a"
	echo -e "    2) \e]8;;https://extensions.gnome.org/extension/1031/topicons/\aTopIcons Plus\e]8;;\a"
	echo -e "\nNote: you may want these supporting packages\n'sudo apt install gnome-tweaks gnome-shell-extension-appindicator gir1.2-appindicator3-0.1'"
}

function reset_mutter_overlay_key {
	if [[ $(gsettings get org.gnome.mutter overlay-key | grep "''\|' '" | wc -l) != 1 ]]; then
		bound=$(gsettings get org.gnome.mutter overlay-key)
		echo "Overlay key, " $bound ", detected. Will be removing so Super-Space can remap to Cmd-Space for app launching.."
		gsettings set org.gnome.mutter overlay-key ''
	fi
}

function set_show_desktop_shortcut_if_applicable {
	if [[ $(gsettings get org.gnome.desktop.wm.keybindings show-desktop | grep "\[\]" | wc -l) == 1 ]]; then
		gsettings set org.gnome.desktop.wm.keybindings show-desktop "['<Super>d']"
	else
		if [[ $(gsettings get org.gnome.desktop.wm.keybindings show-desktop | grep "<Super>d" | wc -l) == 0 ]]; then
			echo 'Kinto will not set your "Show Desktop" hotkey due to it already being set.\nPlease set Show Desktop to Super-D, or Edit Kinto'"'"'s config.'
			echo "Did not run the following."
			echo "gsettings set org.gnome.desktop.wm.keybindings show-desktop \"['<Super>d']\""
		fi
	fi
}
