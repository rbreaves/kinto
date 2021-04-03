#!/usr/bin/env bash

# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rbreaves/kinto/master/install/linux.sh)"

curl https://github.com/rbreaves/kinto/archive/refs/heads/master.zip -J -L -o ~/Downloads/kinto.zip
unzip ~/Downloads/kinto.zip -d ~/Downloads/
cd ~/Downloads/kinto-master/

kintorelease=`curl -s https://api.github.com/repos/rbreaves/kinto/releases/latest | awk -F'tag_name": ' '{if ($2) print $2}' | tr -d \",`
kintohash=`unzip -z ~/Downloads/kinto.zip | tail -n1`
kintoshort=${kintohash::7}

echo "$kintorelease" "build" "$kintoshort" > ./dl_version

if [ $# -eq 0 ];then
	echo "Installing Kinto..."
	./setup.py
elif [ $1 == "-r" ];then
	echo "Uninstall Kinto..."
	./setup.py -r
fi