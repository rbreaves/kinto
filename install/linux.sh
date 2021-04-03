#!/usr/bin/env bash

# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rbreaves/kinto/master/install/linux.sh)"

curl https://github.com/rbreaves/kinto/archive/refs/heads/master.zip -J -L -o ~/Downloads/kinto.zip
unzip ~/Downloads/kinto.zip -d ~/Downloads/
cd ~/Downloads/kinto-master/

if [ $# -eq 0 ];then
	echo "Installing Kinto..."
	./setup.py
elif [ $1 == "-r" ];then
	echo "Uninstall Kinto..."
	./setup.py -r
fi