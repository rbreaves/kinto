#!/usr/bin/env bash

typeset -l distro
distro=$(awk -F= '$1=="NAME" { gsub("[\",!,_, ]","",$2);print $2 ;}' /etc/os-release)
packages=""

function unipkg() {
	if pkgmgr="$( which apt-get )" 2> /dev/null; then
		echo "Debian"
		$pkgmgr update
		$pkgmgr --yes --force-yes install $1
	elif pkgmgr="$( which dnf )" 2> /dev/null; then
		echo "dnf"
		$pkgmgr check-update; $pkgmgr install -y $1
	elif pkgmgr="$( which pacman )" 2> /dev/null; then
		echo "Arch-based"
		$pkgmgr -Syy;yes | $pkgmgr -S $1
	else
		echo "Package manager not found, please install $1" >&2
	fi
	if [[ 1 -ne $# ]]; then
		echo "Syntax: $0 PACKAGE"
	fi
}

if ! [ -x "$(command -v git)" ]; then
	packages="${packages} git"
fi

if ! [ -x "$(command -v xhost)" ] || ! [ -x "$(command -v gcc)" ]; then
	if [ "$distro" == "manjarolinux" ]; then
		packages="xorg-xhost gcc"
	fi
fi

if ! [ -x "$(command -v pip3)" ]; then
	if [ "$distro" == "manjarolinux" ]; then
		echo "Will need to install python-pip..."
		packages="${packages} python-pip"
	else
		echo "Will need to install python3-pip..."
		packages="${packages} python3-pip"
	fi
fi

if ! [ -x "$(command -v python3-config)" ]; then
	if [ "$distro" == "ubuntu" ] || [ "$distro" == "debian" ] || [ "$distro" == 'linuxmint' ]; then
		packages="${packages} python3-dev"
	elif [ "$distro" == "fedora" ]; then
		packages="${packages} python3-devel"
	fi
fi

if [ "$packages" != "" ]; then
	sudo unipkg "${packages}"
fi

git clone https://github.com/rbreaves/kinto.git /tmp/kinto
cd /tmp/kinto
./setup.py