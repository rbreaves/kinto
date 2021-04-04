#!/bin/bash

if pkgmgr="$( which apt-get )" 2> /dev/null; then
   echo 
   echo "Debian apt-get package manager detected... "
   echo "Installing $1... "
   echo 
   $pkgmgr update
   $pkgmgr --yes install $1
elif pkgmgr="$( which dnf )" 2> /dev/null; then
   echo 
   echo "dnf package manager detected... "
   echo "Installing $1... "
   echo 
   $pkgmgr check-update; $pkgmgr install -y $1
elif pkgmgr="$( which pacman )" 2> /dev/null; then
   echo 
   echo "Arch-based pacman package manager detected... "
   echo "Installing $1... "
   echo 
   $pkgmgr -Syy;yes | $pkgmgr -S $1
elif pkgmgr="$( which zypper )" 2> /dev/null; then
   echo 
   echo "zypper package manager detected... "
   echo "Installing $1... "
   echo 
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
