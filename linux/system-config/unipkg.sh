#!/bin/bash

if pkgmgr="$( which apt-get )" 2> /dev/null; then
   echo "Debian"
   $pkgmgr update
   $pkgmgr --yes --allow-downgrades --allow-remove-essential --allow-change-held-packages install $1
elif pkgmgr="$( which dnf )" 2> /dev/null; then
   echo "dnf"
   $pkgmgr check-update; $pkgmgr install -y $1
elif pkgmgr="$( which pacman )" 2> /dev/null; then
   echo "Arch-based"
   $pkgmgr -Syy;yes | $pkgmgr -S $1
elif pkgmgr="$( which zypper )" 2> /dev/null; then
   echo "openSUSE"
   $pkgmgr refresh
   $pkgmgr -n install $1
else
   echo "Package manager not found, please install $1" >&2
   exit 1
fi
if [[ 1 -ne $# ]]; then
   echo "Syntax: $0 PACKAGE"
   exit 1
fi
exit $?
